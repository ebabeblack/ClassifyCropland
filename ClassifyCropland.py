import arcpy
from arcpy.sa import *
from arcpy.ia import *
from math import log
# Function to summarize cropland diversity in given geometries
def SummarizeCropland(USDA_TIF, Boundaries, Analysis_Feature_Class, Area_Analysis_Field, Output_Folder):
    arcpy.env.overwriteOutput = True
    arcpy.management.Delete("in_memory")
    
    # Check out necessary licenses
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("Spatial")
    arcpy.CheckOutExtension("ImageAnalyst")
    
    # Get spatial references
    tif_sr = arcpy.Describe(USDA_TIF).spatialReference
    boundaries_sr = arcpy.Describe(Boundaries).spatialReference
    analysis_fc_sr = arcpy.Describe(Analysis_Feature_Class).spatialReference
    
    # Check if all spatial references match
    if tif_sr.name != boundaries_sr.name or tif_sr.name != analysis_fc_sr.name:
        raise ValueError("All inputs must have the same spatial reference system. Please reproject the data before running.")
    
    print("Spatial references match.")
    
    # Clip the county features to the boundary extent
    county_clip = arcpy.analysis.Clip(Analysis_Feature_Class, Boundaries, f"{Output_Folder}/county_clip")
    print(f"County features clipped: {county_clip}")
    
    # Perform raster processing by clipping directly
    crop_clip_raster = arcpy.management.Clip(USDA_TIF, Boundaries, "in_memory/crop_clip")
    crop_clip_raster = Raster("in_memory/crop_clip")
    print("Raster clipped and treated as a Raster object.")
    
    # Reclassify the raster values
    reclass_raster = Con(
        ((crop_clip_raster >= 1) & (crop_clip_raster <= 57)) |
        ((crop_clip_raster >= 65) & (crop_clip_raster <= 81)) |
        ((crop_clip_raster >= 113) & (crop_clip_raster <= 120)) |
        ((crop_clip_raster >= 125) & (crop_clip_raster <= 250)), 
        crop_clip_raster, 
        SetNull(crop_clip_raster, crop_clip_raster)
    )
    reclass_raster.save("in_memory/reclass_crop")
    print("Raster reclassified.")
    
    # Perform Zonal Statistics
    zonal_stats = ZonalStatisticsAsTable(county_clip, Area_Analysis_Field, reclass_raster, f"{Output_Folder}/zonal_stats", "DATA", "VARIETY")
    print("Zonal statistics calculated.")
    
    # Summarize Categorical Raster
    summarized_raster = SummarizeCategoricalRaster(reclass_raster, f"{Output_Folder}/summarized_raster", "", county_clip, Area_Analysis_Field)
    print("Categorical raster summarized.")
    
    # Join and export the summary table
    joined_view = arcpy.management.AddJoin(summarized_raster, Area_Analysis_Field, zonal_stats, Area_Analysis_Field, "KEEP_COMMON")
    print("Join operation completed.")
    
    # Check the fields in the joined view
    print(f"Fields in joined view: {[f.name for f in arcpy.ListFields(joined_view)]}")
    summary_table = f"{Output_Folder}/Table_Raster_Summary"
    arcpy.conversion.ExportTable(joined_view, summary_table)
    print(f"Summary table exported: {summary_table}")
    
    # Process the summary table
    table1 = add_prop_fields(summary_table)
    table2 = add_sum_field(table1)
    table3 = calculate_evenness(table2)
    table4 = clean_diversity(table3)
    
    # Save the processed table
    processed_summary_table = f"{Output_Folder}/Processed_Table_Raster_Summary"
    arcpy.Copy_management(table4, processed_summary_table)
    print(f"Processed summary table saved: {processed_summary_table}")
    
    # Create the feature layer for county_clip
    arcpy.management.MakeFeatureLayer(f"{Output_Folder}/county_clip", "county_clip_layer")
    print("Feature layer created for county_clip.")
    
    # Join the processed summary table to the county_clip
    biodiversity_areas = f"{Output_Folder}/Biodiversity_Areas"
    arcpy.management.AddJoin("county_clip_layer", Area_Analysis_Field, processed_summary_table, Area_Analysis_Field)
    arcpy.conversion.FeatureClassToFeatureClass("county_clip_layer", Output_Folder, "Biodiversity_Areas")
    print("Processed summary table joined to county_clip.")
    
    # Clean up in-memory layers
    arcpy.management.Delete("in_memory")
    print("In-memory layers cleaned up.")
    
    print("Cropland diversity summary completed. Outputs saved to:")
    print(f"- {Output_Folder}/Biodiversity_Areas")
# Function to add proportional fields
def add_prop_fields(table):
    fields = arcpy.ListFields(table)
    new_field_names = [field.name for field in fields if field.name.startswith("C_")]
    with arcpy.da.UpdateCursor(table, new_field_names + ["COUNT"]) as cursor:
        for row in cursor:
            for i in range(len(new_field_names)):
                c_value = row[i]
                count_value = row[-1]
                # Check if c_value or count_value is None
                if c_value is not None and count_value is not None and count_value != 0:
                    ratio = c_value / count_value
                    row[i] = -ratio / log(ratio) if ratio > 0 else 0
                else:
                    row[i] = 0  # Set to 0 if c_value or count_value is None or count_value is 0
            cursor.updateRow(row)
    return table  # Return the updated table
# Function to add sum field
def add_sum_field(table):
    c_fields = [field.name for field in arcpy.ListFields(table) if field.name.startswith("C_")]
    arcpy.AddField_management(table, "Sum_C", "DOUBLE")
    with arcpy.da.UpdateCursor(table, c_fields + ["Sum_C"]) as cursor:
        for row in cursor:
            row[-1] = sum(row[:-1])  
            cursor.updateRow(row)
    return table  # Return the updated table
# Function to calculate evenness
def calculate_evenness(table):
    # Retrieve the VARIETY value
    with arcpy.da.SearchCursor(table, ["VARIETY"]) as cursor:
        variety_value = next(cursor)[0]
    variety_log = log(variety_value) if variety_value else 1  # Avoid log(0) and ensure variety_log is a valid number
    arcpy.AddField_management(table, "EVENNESS", "DOUBLE")
    with arcpy.da.UpdateCursor(table, ["Sum_C", "EVENNESS"]) as cursor:
        for row in cursor:
            sum_c_value = row[0]
            if sum_c_value is not None and variety_log != 0:
                evenness = sum_c_value / variety_log
            else:
                evenness = 0  # Set evenness to 0 if sum_c_value is None or variety_log is 0
            row[1] = evenness
            cursor.updateRow(row)
    return table  # Return the updated table
def clean_diversity(table):
    # List all fields in the table
    fields = arcpy.ListFields(table)
    
    # Identify fields that start with 'C_'
    c_fields = [field.name for field in fields if field.name.startswith("C_")]
    
    # Remove fields that start with 'C_'
    for field in c_fields:
        arcpy.DeleteField_management(table, field)
    
    return table  # Return the cleaned table
# Main function to execute the script tool
def main():
    # Define script tool parameters
    USDA_TIF = arcpy.GetParameterAsText(0)
    Boundaries = arcpy.GetParameterAsText(1)
    Analysis_Feature_Class = arcpy.GetParameterAsText(2)
    Area_Analysis_Field = arcpy.GetParameterAsText(3)
    Output_Folder = arcpy.GetParameterAsText(4)
    
    # Call the SummarizeCropland function with the parameters
    SummarizeCropland(USDA_TIF, Boundaries, Analysis_Feature_Class, Area_Analysis_Field, Output_Folder)
# Execute the main function
if __name__ == "__main__":
    main()


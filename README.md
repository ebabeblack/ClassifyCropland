# Classify Cropland

## Introduction

Using the Tool in ArcGIS
What I've done in this Repo is put the code for the script tool I created, the code can be manually copied into your ArcGIS environment, you'll have to manually set parameters!:

## Repo Organization
- **ClassifyCropland.py** is just the python script that the tool uses. Feel free to copy this into a tool within your own environment and manually adjust the inputs

### Open the Tool:

In the ArcGIS Pro project, navigate to the toolbox where the "Summarize Cropland" tool is located.
Double-click the "Summarize Cropland" tool to open it.
Set the Inputs:
- **USDA_TIF:** Browse to and select the [USDA NASS Cropland Data](https://developers.google.com/earth-engine/datasets/catalog/USDA_NASS_CDL)  Layers TIFF file.

- **Boundaries:** Browse to and select the boundaries feature layer (e.g., a shapefile or feature class).
- **Analysis_Feature_Class:** Browse to and select the feature layer containing the analysis features.
- **Area_Analysis_Field:** Select the field in the Analysis_Feature_Class used for area analysis.
- **Output_Folder:** Browse to and select the folder where the output will be saved.

### Run the Tool:

Click "Run" to execute the tool. The tool will process the data, calculate the biodiversity metrics, and save the results to the specified output folder.
## Inputs
#### USDA_TIF (Raster Dataset)
##### Description: 
This is a raster dataset from the USDA NASS Cropland Data Layers (CDL). It contains categorical data representing different land uses and crop types.
Example: C:/data/usda_raster.tif
#### Boundaries (Feature Layer)
##### Description: 
This is a feature layer representing the geographic boundaries within which the analysis will be conducted. It could be a shapefile or feature class containing polygons.
Example: C:/data/boundaries.shp
#### Analysis_Feature_Class (Feature Layer)
##### Description: 
This is a feature layer that contains the specific features (e.g., counties, regions) within the boundaries where the analysis will be performed.
Example: C:/data/analysis_features.shp
#### Area_Analysis_Field (Field)
##### Description: 
This is the name of the field in the Analysis_Feature_Class that will be used for area analysis. This field typically contains unique identifiers for each region.
Example: AREA_FIELD
#### Output_Folder (Folder)
##### Description: 
This is the folder where the output feature class will be saved. The output will include the calculated biodiversity metrics (VARIETY and EVENNESS) for each analysis area.
Example: C:/output

#### Acknowledgments
USDA NASS for providing the Cropland Data Layers.
ArcGIS for providing the necessary tools and libraries.
Links
USDA NASS CDL
GEE Viewer

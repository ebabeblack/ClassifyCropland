# Classify Cropland

## Introduction

Using the Tool in ArcGIS
What I've done in this Repo (**ClassifyCropland.py**) is put the code for the script tool I created, the code can be manually copied into your ArcGIS environment, you'll have to manually set parameters!:

## Setting Up the Tool Manually

To set up the "Classify Cropland" tool manually in ArcGIS, follow these steps:

### 1. Download and Prepare Your Data

Ensure you have the following data files ready and properly georeferenced:

- **USDA NASS Cropland Data Layers (CDL)**: Download the raster dataset in TIFF format.
- **Boundaries**: A feature layer (e.g., shapefile or feature class) representing the geographic boundaries within which the analysis will be conducted.
- **Analysis Feature Class**: A feature layer containing the specific features (e.g., counties, regions) within the boundaries where the analysis will be performed.

### 2. Organize Input Parameters

You will need to configure the following input parameters for the tool. Make sure to provide accurate paths and field names:

#### USDA_TIF (Raster Dataset)

- **Description**: This is a raster dataset from the USDA NASS Cropland Data Layers (CDL). It contains categorical data representing different land uses and crop types. The code can be easily adjusted to work on any catagorical raster. (Let me know if you do!)
- **Example Path**: `C:/data/usda_raster.tif`

#### Boundaries (Feature Layer)

- **Description**: This is a feature layer representing the geographic boundaries within which the analysis will be conducted. It could be a shapefile or feature class containing polygons.
- **Example Path**: `C:/data/boundaries.shp`

#### Analysis_Feature_Class (Feature Layer)

- **Description**: This is a feature layer that contains the specific features (e.g., counties, regions) within the boundaries where the analysis will be performed.
- **Example Path**: `C:/data/analysis_features.shp`

#### Area_Analysis_Field (Field)

- **Description**: This is the name of the field in the `Analysis_Feature_Class` that will be used for area analysis. This field typically contains unique identifiers for each region.
- **Example Field Name**: `AREA_FIELD`

#### Output_Folder (Folder)

- **Description**: This is the folder where the output feature class will be saved. The output will include the calculated biodiversity metrics (VARIETY and EVENNESS) for each analysis area.
- **Example Path**: `C:/output`

### 3. Add the Script Tool to ArcGIS

1. **Open ArcGIS Pro** and create a new project or open an existing project.
2. **Add a Toolbox**:
   - Right-click on "Toolboxes" in the Catalog pane.
   - Select "Add Toolbox" and navigate to where you want to create the new toolbox.
   - Name the toolbox (e.g., `CroplandAnalysis.tbx`).
3. **Create a New Script Tool**:
   - Right-click the newly created toolbox and select "New" > "Script".
   - Name the script tool (e.g., `Summarize Cropland`).
   - Follow the prompts to link the script tool to the `ClassifyCropland.py` script.
4. **Define the Tool Parameters**:
   - Open the script tool's properties and configure the parameters as follows:

     | Parameter Name       | Data Type          | Direction | Default         | Filter          | Required |
     |----------------------|--------------------|-----------|-----------------|-----------------|----------|
     | USDA_TIF             | Raster Dataset     | Input     |                 |                 | Yes      |
     | Boundaries           | Feature Layer      | Input     |                 |                 | Yes      |
     | Analysis_Feature_Class | Feature Layer    | Input     |                 |                 | Yes      |
     | Area_Analysis_Field  | Field              | Input     |                 | Field from Analysis_Feature_Class | Yes |
     | Output_Folder        | Workspace          | Input     |                 | Folder          | Yes      |

5. **Save and Run the Tool**:
   - Save the changes and close the properties.
   - Run the tool by double-clicking it, providing the necessary inputs, and executing the analysis.

By following these steps, you will manually set up the "Classify Cropland" tool in ArcGIS and be able to perform the analysis as intended.

## Acknowledgments

- USDA NASS for providing the Cropland Data Layers.
- ArcGIS for providing the necessary tools and libraries.

## Links

- [USDA NASS CDL](https://developers.google.com/earth-engine/datasets/catalog/USDA_NASS_CDL)
- [GEE Viewer](https://code.earthengine.google.com/8d92850325c6389f44bde1764c013846)

#### Acknowledgments
USDA NASS for providing the Cropland Data Layers.
ArcGIS for providing the necessary tools and libraries.
Links
USDA NASS CDL
GEE Viewer

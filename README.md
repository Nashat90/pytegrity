# Well Integrity Visualization Tool

# pytegrity

`pytegrity` 
This application allows users to upload LAS files, visualize well integrity, and extract finger logs to analyze data related to Well integrity issues (Corrosion, Deposition, etc).

## Requirements
Before running the app, make sure to install the following libraries:

```bash
pip install streamlit lasio pandas plotly pytegrity
``` 

![Interactive application](images/stream.png)

## Features
File Upload: Upload LAS files for analysis.

Finger Log Selection: Choose which finger/pad logs to visualize.

Depth Range Control: Adjust the depth range for the plot using a slider.

Plot Customization: Customize the plot's height and width.

Well Integrity Visualization: View a detailed plot representing the well integrity with selected logs and depth ranges.

## Usage
Upload LAS File:

On the sidebar, click the "Upload LAS File" button to upload your LAS file.

The file is temporarily stored for processing.
![Interactive notebook](images/jup.png)
## Select Finger Logs:

Choose the desired finger logs to include in the visualization.

Adjust Depth Range:

Use the depth range slider to select the depth interval to visualize.

## Plot Customization:

Set the height and width of the plot for better visualization.

## Visualization:

After selecting your preferences, the app will generate the well integrity plot based on the LAS file data.

Code Breakdown
File Upload:
The file_uploader method is used to upload LAS files, and the uploaded file is saved temporarily for further processing.

Data Loading:
The LAS file is read using the lasio library and converted to a pandas DataFrame.

Finger Log Selection:
Users can select columns that contain "FING" to display the desired finger logs.

Depth Range Selection:
The depth range for visualization is controlled through the sidebar slider, adjusting the Y-axis range on the plot.

Visualization:
The plot_well_integrity method from the pytegrity module is used to plot well integrity data. The plot is generated dynamically with customizable height and width.

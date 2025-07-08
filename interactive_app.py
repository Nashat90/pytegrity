import streamlit as st
import lasio as ls
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pytegrity.tubular_integrity as ti  # Assuming this is the module you created
import tempfile
import shutil

# Streamlit App Layout
#st.title("Well Integrity Visualization Tool")

# Step 1: File Upload
uploaded_file = st.sidebar.file_uploader("Upload LAS File", type=["LAS"])

if uploaded_file is not None:
    # Step 2: Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".LAS") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())  # Write the binary content to a temporary file
        tmp_file_path = tmp_file.name  # Get the path of the temporary file

    # Step 3: Read the LAS file using lasio
    las = ls.read(tmp_file_path)
    data = las.df()  # Convert LAS data to a pandas DataFrame
    
    # Step 4: Extract finger logs (columns containing "FING")
    fingers = [col for col in data.columns if "FING" in col]

    fingers =st.sidebar.multiselect("Select Fingers/Pads", data.columns,default=fingers)
    st.write("Data Loaded")
    # Step 5: Y-Axis Depth Range Control
    min_depth, max_depth = data.index.min(), data.index.max()
    depth_range = st.sidebar.slider("Select Depth Range", min_value=int(min_depth), max_value=int(max_depth),
                            value=(int(min_depth), int(max_depth)))
    ht = st.sidebar.slider("Height",100,10000,1000)
    wd = st.sidebar.slider("Width",100,2000,1000)
    # Step 7: Plot Well Integrity (Plotting function)
    if uploaded_file is not None:
        with st.spinner('Generating plots...'):
            # Plot well integrity using the function from pytegrity
            fig = ti.plot_well_integrity(
                las_file_as_df=data,
                fingers=fingers,
                plotly_template="plotly_white",
                height=ht, width=wd
            )

            # Adjust depth range based on slider input
            fig.update_yaxes(range=[depth_range[0], depth_range[1]])

            # Display plot
            st.plotly_chart(fig)

    # Clean up: Delete the temporary file after it's used
    #shutil.rmtree(tmp_file_path)

else:
    st.warning("Please upload a LAS file to begin.")

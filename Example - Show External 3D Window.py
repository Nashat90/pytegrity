# External Interactive 3D Window
import lasio as ls
#read las files
las = ls.read(r"D:\Training Pool\Python for Production Optimization and Field Development\All Codes\17-Multi Finger Caliper Visualization [Las File]\mfc.LAS")
df = las.df() # convert to dataframe
fing = []
#Select fingers
for col in df.columns:
    if "FING" in col:
        fing.append(col)

import pytegrity.tubular_integrity as ti
ti.plot_3d_window(df, fing) # show  the 3D window

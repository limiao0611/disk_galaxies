import yt
import numpy as np

# Load the dataset.
a="63"
ds = yt.load("DD00"+a+"/sb_00"+a)

# Create a data container (like a sphere or region) that
# represents the entire domain.
ad = ds.all_data()

# Get the minimum and maximum densities.
quan="density"
mi, ma = ad.quantities.extrema(quan)

# Create a transfer function to map field values to colors.
# We bump up our minimum to cut out some of the background fluid
tf = yt.ColorTransferFunction((np.log10(mi)+1, np.log10(ma)))

# Add five Gaussians, evenly spaced between the min and
# max specified above with widths of 0.02 and using the
# spectral colormap.
tf.add_layers(5, w=0.02, colormap="spectral")

# Choose a center for the render.
c = [0.5, 0.5, 0.5]

# Choose a vector representing the viewing direction.
L = [0.5, 0.2, 0.7]

# Set the width of the image.
# Decreasing or increasing this value
# results in a zoom in or out.
W = 1.0

# The number of pixels along one side of the image.
# The final image will have Npixel^2 pixels.
Npixels = 512

# Create a camera object.
# This object creates the images and
# can be moved and rotated.
cam = ds.camera(c, L, W, Npixels, tf)

# Create a snapshot.
# The return value of this function could also be accepted, modified (or saved
# for later manipulation) and then put written out using write_bitmap.
# clip_ratio applies a maximum to the function, which is set to that value
# times the .std() of the array.
cam.snapshot(a+"_volume_rendered_"+quan+"_.png", clip_ratio=8.0)

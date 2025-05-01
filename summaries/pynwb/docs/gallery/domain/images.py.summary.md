# Storing Image Data in NWB

This document explains how to use the `pynwb.image` module to add different types of images to an NWBFile.

## Image Types and Containers

- **OpticalSeries**: For time series of images presented as stimuli
- **ImageSeries**: For general time series of images (acquired during experiments)
- **GrayscaleImage**: For static grayscale images
- **RGBImage**: For static color images
- **RGBAImage**: For static color images with transparency
- **AbstractFeatureSeries**: For storing features of visual stimuli

## Usage Examples

### Basic Setup
```python
from datetime import datetime
import numpy as np
from pynwb import NWBHDF5IO, NWBFile
from pynwb.base import Images
from pynwb.image import GrayscaleImage, ImageSeries, OpticalSeries, RGBAImage, RGBImage
from pynwb.misc import AbstractFeatureSeries

# Create NWBFile
nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=session_start_time,
    experimenter=["Baggins, Bilbo"],
    lab="Bag End Laboratory",
    institution="University of Middle Earth at the Shire",
    experiment_description="I went on an adventure to reclaim vast treasures.",
    session_id="LONELYMTN001",
)
```

### Storing Stimulus Images (OpticalSeries)
```python
image_data = np.random.randint(low=0, high=255, size=(200, 50, 50, 3), dtype=np.uint8)
optical_series = OpticalSeries(
    name="StimulusPresentation",
    distance=0.7,
    field_of_view=[0.2, 0.3, 0.7],
    orientation="lower left",
    data=image_data,
    unit="n.a.",
    format="raw",
    starting_frame=[0.0],
    rate=1.0,
    description="The images presented to the subject as stimuli",
)
nwbfile.add_stimulus(stimulus=optical_series)
```

### Storing Stimulus Features (AbstractFeatureSeries)
```python
feature_data = np.random.rand(200, 3)  # 200 time points, 3 features
abstract_feature_series = AbstractFeatureSeries(
    name="StimulusFeatures",
    data=feature_data,
    timestamps=np.linspace(0, 1, 200),
    description="Features of the visual stimuli",
    features=["luminance", "contrast", "spatial frequency"],
    feature_units=["n.a.", "n.a.", "cycles/degree"],
)
nwbfile.add_stimulus(abstract_feature_series)
```

### Storing Acquired Image Series (ImageSeries)
```python
image_data = np.random.randint(low=0, high=255, size=(200, 50, 50, 3), dtype=np.uint8)
behavior_images = ImageSeries(
    name="ImageSeries",
    data=image_data,
    description="Image data of an animal moving in environment.",
    unit="n.a.",
    format="raw",
    rate=1.0,
    starting_time=0.0,
)
nwbfile.add_acquisition(behavior_images)
```

### External Image Files
```python
external_file = [os.path.relpath(movie_path, nwbfile_path) for movie_path in moviefiles_path]
timestamps = [0.0, 0.04, 0.07, 0.1, 0.14, 0.16, 0.21]
behavior_external_file = ImageSeries(
    name="ExternalFiles",
    description="Behavior video of animal moving in environment.",
    unit="n.a.",
    external_file=external_file,
    format="external",
    starting_frame=[0, 2, 4],
    timestamps=timestamps,
)
nwbfile.add_acquisition(behavior_external_file)
```

### Static Images
```python
# RGBA Image
rgba_logo = RGBAImage(
    name="pynwb_RGBA_logo",
    data=np.array(img),  # 3D array with RGBA values
    resolution=70.0,  # in pixels/cm
    description="RGBA version of the PyNWB logo.",
)

# RGB Image
rgb_logo = RGBImage(
    name="pynwb_RGB_logo",
    data=np.array(img.convert("RGB")),  # 3D array with RGB values
    resolution=70.0,
    description="RGB version of the PyNWB logo.",
)

# Grayscale Image
gs_logo = GrayscaleImage(
    name="pynwb_Grayscale_logo",
    data=np.array(img.convert("L")),  # 2D array
    description="Grayscale version of the PyNWB logo.",
    resolution=35.433071,
)

# Group images in an Images container
images = Images(
    name="logo_images",
    images=[rgb_logo, rgba_logo, gs_logo],
    description="A collection of logo images presented to the subject.",
)
nwbfile.add_acquisition(images)
```

### IndexSeries for Repeated Images
```python
from pynwb.base import ImageReferences
from pynwb.image import IndexSeries

images = Images(
    name="raccoons",
    images=[rgb_logo, gs_logo],
    description="A collection of raccoons.",
    order_of_images=ImageReferences("order_of_images", [rgb_logo, gs_logo]),
)

idx_series = IndexSeries(
    name="stimuli",
    data=[0, 1, 0, 1],  # Indexes into the Images container
    indexed_images=images,
    unit="N/A",
    timestamps=[0.1, 0.2, 0.3, 0.4],
)
```

### Writing and Reading
```python
# Writing
with NWBHDF5IO(nwbfile_path, "w") as io:
    io.write(nwbfile)

# Reading
with NWBHDF5IO(nwbfile_path, "r") as io:
    read_nwbfile = io.read()
    # Access acquisition data
    read_nwbfile.acquisition["ImageSeries"]
    # Access stimulus data
    read_nwbfile.stimulus["StimulusPresentation"].data[:]
```
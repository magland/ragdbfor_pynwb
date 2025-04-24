This document provides a tutorial on writing calcium imaging data to NWB files using pynwb. The workflow includes creating an imaging plane, adding acquired two-photon images, adding motion correction (optional), adding image segmentation, and adding fluorescence and dF/F responses.

**Creating the NWB File:**

The first step is creating the `NWBFile` object using the `pynwb.file.NWBFile` class.

```python
from datetime import datetime
from uuid import uuid4
from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter=[
        "Baggins, Bilbo",
    ],
    lab="Bag End Laboratory",
    institution="University of Middle Earth at the Shire",
    experiment_description="I went on an adventure to reclaim vast treasures.",
    keywords=["ecephys", "exploration", "wanderlust"],
    related_publications="doi:10.1016/j.neuron.2016.12.011",
)
```

**Imaging Plane:**

An `ImagingPlane` object is created to store information about the optical imaging data.  This requires creating a `Device` object for the microscope and an `OpticalChannel` object.

```python
from pynwb.ophys import OpticalChannel

device = nwbfile.create_device(
    name="Microscope",
    description="My two-photon microscope",
    manufacturer="Loki Labs",
    model_number="ABC-123",
    model_name="Loki 1.0",
    serial_number="1234567890",
)
optical_channel = OpticalChannel(
    name="OpticalChannel",
    description="an optical channel",
    emission_lambda=500.0,
)
```

Then, create an `ImagingPlane` object:

```python
imaging_plane = nwbfile.create_imaging_plane(
    name="ImagingPlane",
    optical_channel=optical_channel,
    imaging_rate=30.0,
    description="a very interesting part of the brain",
    device=device,
    excitation_lambda=600.0,
    indicator="GFP",
    location="V1",
    grid_spacing=[0.01, 0.01],
    grid_spacing_unit="meters",
    origin_coords=[1.0, 2.0, 3.0],
    origin_coords_unit="meters",
)
```

**One-photon Series:**

A `OnePhotonSeries` object stores raw one-photon imaging data. Add the `OnePhotonSeries` objects to the `NWBFile` as acquired data.

```python
from pynwb.ophys import OnePhotonSeries
import numpy as np

one_p_series = OnePhotonSeries(
    name="OnePhotonSeries",
    description="Raw 1p data",
    data=np.ones((1000, 100, 100)),
    imaging_plane=imaging_plane,
    rate=1.0,
    unit="normalized amplitude",
)

nwbfile.add_acquisition(one_p_series)
```

**Two-photon Series:**

`TwoPhotonSeries` objects store acquired two-photon imaging data, similar to `OnePhotonSeries`.

```python
from pynwb.ophys import TwoPhotonSeries

two_p_series = TwoPhotonSeries(
    name="TwoPhotonSeries",
    description="Raw 2p data",
    data=np.ones((1000, 100, 100)),
    imaging_plane=imaging_plane,
    rate=1.0,
    unit="normalized amplitude",
)

nwbfile.add_acquisition(two_p_series)
```

**Motion Correction (Optional):**

Motion correction results can be stored using a `MotionCorrection` object, which holds `CorrectedImageStack` objects.

```python
from pynwb import TimeSeries
from pynwb.image import ImageSeries
from pynwb.ophys import CorrectedImageStack, MotionCorrection

corrected = ImageSeries(
    name="corrected",  # this must be named "corrected"
    description="A motion corrected image stack",
    data=np.ones((1000, 100, 100)),
    unit="na",
    format="raw",
    starting_time=0.0,
    rate=1.0,
)

xy_translation = TimeSeries(
    name="xy_translation",
    description="x,y translation in pixels",
    data=np.ones((1000, 2)),
    unit="pixels",
    starting_time=0.0,
    rate=1.0,
)

corrected_image_stack = CorrectedImageStack(
    corrected=corrected,
    original=one_p_series,
    xy_translation=xy_translation,
)

motion_correction = MotionCorrection(corrected_image_stacks=[corrected_image_stack])

from pynwb.base import ProcessingModule

ophys_module = nwbfile.create_processing_module(
    name="ophys", description="optical physiology processed data"
)

ophys_module.add(motion_correction)
```

**Plane Segmentation:**

The `PlaneSegmentation` class stores detected regions of interest (ROIs). It is a subclass of `DynamicTable`.  The `ImageSegmentation` class can contain multiple `PlaneSegmentation` tables.

```python
from pynwb.ophys import ImageSegmentation

img_seg = ImageSegmentation()

ps = img_seg.create_plane_segmentation(
    name="PlaneSegmentation",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,  # optional
)

ophys_module.add(img_seg)
```

**Regions Of Interest (ROIs):**

ROIs can be added to the `PlaneSegmentation` table using image masks, pixel masks, or voxel masks.

*   **Image masks:** An array the same size as a single frame, indicating the mask weight of each pixel.

```python
for _ in range(30):
    image_mask = np.zeros((100, 100))

    # randomly generate example image masks
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)
    image_mask[x:x + 5, y:y + 5] = 1

    # add image mask to plane segmentation
    ps.add_roi(image_mask=image_mask)
```

*   **Pixel masks:** An array of triplets (x, y, weight) that have a non-zero weight.

```python
ps2 = img_seg.create_plane_segmentation(
    name="PlaneSegmentation2",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,  # optional
)

for _ in range(30):
    # randomly generate example starting points for region
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)

    # define an example 4 x 3 region of pixels of weight '1'
    pixel_mask = []
    for ix in range(x, x + 4):
        for iy in range(y, y + 3):
            pixel_mask.append((ix, iy, 1))

    # add pixel mask to plane segmentation
    ps2.add_roi(pixel_mask=pixel_mask)
```

*   **Voxel masks:** An array of quadruplets (x, y, z, weight) that have a non-zero weight.

```python
ps3 = img_seg.create_plane_segmentation(
    name="PlaneSegmentation3",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,  # optional
)

from itertools import product

for _ in range(30):
    # randomly generate example starting points for region
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)
    z = np.random.randint(0, 15)

    # define an example 4 x 3 x 2 voxel region of weight '0.5'
    voxel_mask = []
    for ix, iy, iz in product(
        range(x, x + 4),
        range(y, y + 3),
        range(z, z + 2)
    ):
        voxel_mask.append((ix, iy, iz, 0.5))

    # add voxel mask to plane segmentation
    ps3.add_roi(voxel_mask=voxel_mask)
```

**Storing Fluorescence Measurements:**

Fluorescence data is stored using `RoiResponseSeries`. A `DynamicTableRegion` is used to reference ROIs in the `PlaneSegmentation` table.

```python
from pynwb.ophys import Fluorescence, RoiResponseSeries

rt_region = ps.create_roi_table_region(
    region=[0, 1], description="the first of two ROIs"
)

roi_resp_series = RoiResponseSeries(
    name="RoiResponseSeries",
    description="Fluorescence responses for two ROIs",
    data=np.ones((50, 2)),  # 50 samples, 2 ROIs
    rois=rt_region,
    unit="lumens",
    rate=30.0,
)

fl = Fluorescence(roi_response_series=roi_resp_series)
ophys_module.add(fl)
```

To store dF/F data instead of fluorescence data, store the `RoiResponseSeries` object in a `DfOverF` object in a similar way.

**Write and Read the File:**

```python
from pynwb import NWBHDF5IO

with NWBHDF5IO("ophys_tutorial.nwb", "w") as io:
    io.write(nwbfile)

with NWBHDF5IO("ophys_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()
    print(read_nwbfile.acquisition["TwoPhotonSeries"])
    print(read_nwbfile.processing["ophys"])
    print(read_nwbfile.processing["ophys"]["Fluorescence"])
    print(read_nwbfile.processing["ophys"]["Fluorescence"]["RoiResponseSeries"])
```

**Accessing data regions**
```python
with NWBHDF5IO("ophys_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()

    roi_resp_series = read_nwbfile.processing["ophys"]["Fluorescence"][
        "RoiResponseSeries"
    ]

    print("section of fluorescence responses:")
    print(roi_resp_series.data[0:10, 0:3])
```

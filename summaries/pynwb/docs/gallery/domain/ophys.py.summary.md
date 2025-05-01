# Calcium Imaging Data in pynwb

This document demonstrates how to use pynwb to work with calcium imaging data. The workflow consists of five main steps:

1. Create an imaging plane
2. Add acquired two-photon images
3. Add motion correction (optional)
4. Add image segmentation
5. Add fluorescence and dF/F responses

## Workflow Steps

### Creating an NWB file
```python
nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter=["Baggins, Bilbo"],
    lab="Bag End Laboratory",
    institution="University of Middle Earth at the Shire",
    experiment_description="I went on an adventure to reclaim vast treasures.",
    keywords=["ecephys", "exploration", "wanderlust"],
    related_publications="doi:10.1016/j.neuron.2016.12.011",
)
```

### Imaging Plane Setup
```python
# Create a Device
device = nwbfile.create_device(
    name="Microscope",
    description="My two-photon microscope",
    manufacturer="Loki Labs",
    model_number="ABC-123",
    model_name="Loki 1.0",
    serial_number="1234567890",
)

# Create an Optical Channel
optical_channel = OpticalChannel(
    name="OpticalChannel",
    description="an optical channel",
    emission_lambda=500.0,
)

# Create an Imaging Plane
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

### Adding One-photon Series
```python
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

### Adding Two-photon Series
```python
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

### Motion Correction (Optional)
```python
corrected = ImageSeries(
    name="corrected",  # must be named "corrected"
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

# Create a processing module for ophys data
ophys_module = nwbfile.create_processing_module(
    name="ophys", description="optical physiology processed data"
)
ophys_module.add(motion_correction)
```

### Plane Segmentation (ROI Definition)
```python
img_seg = ImageSegmentation()

ps = img_seg.create_plane_segmentation(
    name="PlaneSegmentation",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,  # optional
)

ophys_module.add(img_seg)
```

#### Adding ROIs with Image Masks
```python
for _ in range(30):
    image_mask = np.zeros((100, 100))
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)
    image_mask[x:x + 5, y:y + 5] = 1
    ps.add_roi(image_mask=image_mask)
```

#### Adding ROIs with Pixel Masks
```python
ps2 = img_seg.create_plane_segmentation(
    name="PlaneSegmentation2",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,
)

for _ in range(30):
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)
    pixel_mask = []
    for ix in range(x, x + 4):
        for iy in range(y, y + 3):
            pixel_mask.append((ix, iy, 1))
    ps2.add_roi(pixel_mask=pixel_mask)
```

#### Adding ROIs with Voxel Masks (for volumetric imaging)
```python
ps3 = img_seg.create_plane_segmentation(
    name="PlaneSegmentation3",
    description="output from segmenting my favorite imaging plane",
    imaging_plane=imaging_plane,
    reference_images=one_p_series,
)

for _ in range(30):
    x = np.random.randint(0, 95)
    y = np.random.randint(0, 95)
    z = np.random.randint(0, 15)
    voxel_mask = []
    for ix, iy, iz in product(
        range(x, x + 4),
        range(y, y + 3),
        range(z, z + 2)
    ):
        voxel_mask.append((ix, iy, iz, 0.5))
    ps3.add_roi(voxel_mask=voxel_mask)
```

### Storing Fluorescence Measurements
```python
# Create a table region referencing specific ROIs
rt_region = ps.create_roi_table_region(
    region=[0, 1], description="the first of two ROIs"
)

# Create a response series for the fluorescence data
roi_resp_series = RoiResponseSeries(
    name="RoiResponseSeries",
    description="Fluorescence responses for two ROIs",
    data=np.ones((50, 2)),  # 50 samples, 2 ROIs
    rois=rt_region,
    unit="lumens",
    rate=30.0,
)

# Store the response series in a Fluorescence container
fl = Fluorescence(roi_response_series=roi_resp_series)
ophys_module.add(fl)
```

### Writing and Reading the NWB File
```python
# Write the file
with NWBHDF5IO("ophys_tutorial.nwb", "w") as io:
    io.write(nwbfile)

# Read the file
with NWBHDF5IO("ophys_tutorial.nwb", "r") as io:
    read_nwbfile = io.read()
    
    # Access data
    print(read_nwbfile.acquisition["TwoPhotonSeries"])
    print(read_nwbfile.processing["ophys"]["Fluorescence"]["RoiResponseSeries"])
    
    # Access specific data regions
    roi_resp_series = read_nwbfile.processing["ophys"]["Fluorescence"]["RoiResponseSeries"]
    data_slice = roi_resp_series.data[0:10, 0:3]  # Get only a portion of the data
```

Note: For dF/F data, store RoiResponseSeries in a DfOverF object instead of Fluorescence.
# Bruker TIFF Data Conversion with NeuroConv

## Installation

Install NeuroConv with Bruker TIFF support:

```bash
pip install "neuroconv[brukertiff]"
```

## Converting Single Imaging Plane

Use `BrukerTiffSinglePlaneConverter` to convert single-plane data:

```python
from zoneinfo import ZoneInfo
from neuroconv.converters import BrukerTiffSinglePlaneConverter

# Path to folder containing OME-TIF files and XML configuration
folder_path = "path/to/BrukerTif/NCCR32_2023_02_20_Into_the_void_t_series_baseline-000"
converter = BrukerTiffSinglePlaneConverter(folder_path=folder_path)

metadata = converter.get_metadata()
# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"]
tzinfo = ZoneInfo("US/Pacific")
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Run conversion
nwbfile_path = "path/to/save/file.nwb"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

## Converting Multiple Imaging Planes

For volumetric data, use `BrukerTiffMultiPlaneConverter`:

```python
from zoneinfo import ZoneInfo
from neuroconv.converters import BrukerTiffMultiPlaneConverter

# Path to folder containing image data
folder_path = "path/to/BrukerTif/NCCR32_2022_11_03_IntoTheVoid_t_series-005"
# Use "contiguous" for volumetric series or "disjoint" for separate planes
converter = BrukerTiffMultiPlaneConverter(folder_path=folder_path, plane_separation_type="contiguous")

metadata = converter.get_metadata()
# Add timezone information
session_start_time = metadata["NWBFile"]["session_start_time"]
tzinfo = ZoneInfo("US/Pacific")
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Run conversion
nwbfile_path = "output_folder/test2.nwb"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

Note: For multi-plane conversion, `plane_separation_type` can be "contiguous" (for volumetric data) or "disjoint" (for separate imaging planes and two-photon series for each plane).
# Micro-Manager TIFF Data Conversion to NWB

This guide shows how to convert Micro-Manager TIFF imaging data to NWB format using NeuroConv.

## Installation

Install NeuroConv with Micro-Manager TIFF dependencies:

```bash
pip install "neuroconv[micromanagertiff]"
```

## Conversion Process

The conversion utilizes the `MicroManagerTiffImagingInterface` class:

```python
from zoneinfo import ZoneInfo
from neuroconv.datainterfaces import MicroManagerTiffImagingInterface

# Path to folder containing OME-TIF files and DisplaySettings.json
folder_path = OPHYS_DATA_PATH / "imaging_datasets" / "MicroManagerTif" / "TS12_20220407_20hz_noteasy_1"
interface = MicroManagerTiffImagingInterface(folder_path=folder_path, verbose=False)

# Extract metadata
metadata = interface.get_metadata()

# Add timezone information if missing
session_start_time = metadata["NWBFile"]["session_start_time"]
if session_start_time.tzinfo is None:
    tzinfo = ZoneInfo("US/Pacific")
    metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Save as NWB file
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The interface automatically extracts metadata from the Micro-Manager files and converts the imaging data into the standardized NWB format.
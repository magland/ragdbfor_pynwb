# ScanImage Data Conversion to NWB

This document explains how to convert ScanImage ophys data to NWB format using NeuroConv.

## Installation

```bash
pip install "neuroconv[scanimage]"
```

## Converting ScanImage Data

### Single Plane, Single File Imaging Data

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import ScanImageImagingInterface

file_path = OPHYS_DATA_PATH / "imaging_datasets" / "ScanImage" / "scanimage_20220923_roi.tif"
interface = ScanImageImagingInterface(file_path=file_path, channel_name="Channel 1", plane_name="0", verbose=False)

metadata = interface.get_metadata()
# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

### Multi-Plane (Volumetric), Single File Imaging Data

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import ScanImageImagingInterface

file_path = OPHYS_DATA_PATH / "imaging_datasets" / "ScanImage" / "scanimage_20220923_roi.tif"
interface = ScanImageImagingInterface(file_path=file_path, channel_name="Channel 1", verbose=False)

metadata = interface.get_metadata()
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = f"{output_folder}/scanimage_multi_plane.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

### Single Plane, Multi-File (Buffered) Imaging Data

```python
from zoneinfo import ZoneInfo
from neuroconv.datainterfaces import ScanImageMultiFileImagingInterface

folder_path = OPHYS_DATA_PATH / "imaging_datasets" / "ScanImage"
file_pattern = "scanimage_20240320_multifile*.tif"
channel_name = "Channel 1"
interface = ScanImageMultiFileImagingInterface(folder_path=folder_path, file_pattern=file_pattern, channel_name=channel_name, verbose=False)

metadata = interface.get_metadata()
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = f"{output_folder}/scanimage_single_plane_multi_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

### Multi-Plane (Volumetric), Multi-File (Buffered) Imaging Data

```python
from zoneinfo import ZoneInfo
from neuroconv.datainterfaces import ScanImageMultiFileImagingInterface

folder_path = OPHYS_DATA_PATH / "imaging_datasets" / "ScanImage"
file_pattern = "scanimage_20220923_roi.tif"
channel_name = "Channel 1"
interface = ScanImageMultiFileImagingInterface(folder_path=folder_path, file_pattern=file_pattern, channel_name=channel_name, verbose=False)

metadata = interface.get_metadata()
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

nwbfile_path = f"{output_folder}/scanimage_multi_plane_multi_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
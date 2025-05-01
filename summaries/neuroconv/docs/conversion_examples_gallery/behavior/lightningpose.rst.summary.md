# LightningPose Data Conversion to NWB

This document explains how to convert LightningPose pose estimation data to the NWB format.

## Installation

Install NeuroConv with LightningPose dependencies:

```bash
pip install "neuroconv[lightningpose]"
```

## Converting LightningPose Data to NWB

Use the `LightningPoseConverter` class from the `neuroconv.datainterfaces.behavior.lightningpose.lightningposeconverter` module:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.converters import LightningPoseConverter

# Define file paths
folder_path = BEHAVIOR_DATA_PATH / "lightningpose" / "outputs/2023-11-09/10-14-37/video_preds"
file_path = str(folder_path / "test_vid.csv")
original_video_file_path = str(folder_path / "test_vid.mp4")
# The labeled video file path is optional
labeled_video_file_path = str(folder_path / "labeled_videos/test_vid_labeled.mp4")

# Initialize converter
converter = LightningPoseConverter(
    file_path=file_path,
    original_video_file_path=original_video_file_path,
    labeled_video_file_path=labeled_video_file_path,
    verbose=False
)

# Get metadata
metadata = converter.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"]
tzinfo = ZoneInfo("US/Pacific")
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Run the conversion
converter.run_conversion(nwbfile_path=path_to_save_nwbfile, metadata=metadata)
```
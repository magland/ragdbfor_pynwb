# Biocam to NWB Conversion

This guide explains how to convert Biocam electrophysiology data to Neurodata Without Borders (NWB) format using NeuroConv.

## Installation

Install NeuroConv with Biocam dependencies:

```bash
pip install "neuroconv[biocam]"
```

## Conversion Process

Use the `BiocamRecordingInterface` class to convert Biocam data to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import BiocamRecordingInterface

# Specify path to your Biocam file
file_path = "/path/to/your/biocam_hw3.0_fw1.6.brw"
interface = BiocamRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone information
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Specify output path and run conversion
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This code extracts metadata from the Biocam file, adds required session information, and creates an NWB file with the converted data.
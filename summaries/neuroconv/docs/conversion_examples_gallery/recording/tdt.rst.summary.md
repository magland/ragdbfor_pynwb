# Tucker-Davis Technologies (TDT) Data Conversion to NWB

This document explains how to convert Tucker-Davis Technologies (TDT) data to NWB format using the NeuroConv package.

## Installation

Install NeuroConv with TDT-specific dependencies:

```bash
pip install "neuroconv[tdt]"
```

## Converting TDT Data to NWB

The conversion process uses the `TdtRecordingInterface` class:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import TdtRecordingInterface

# Specify the folder containing TDT data
folder_path = f"{ECEPHY_DATA_PATH}/tdt/aep_05"
# Initialize the interface
interface = TdtRecordingInterface(folder_path=folder_path, gain=1.0, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Set required session_start_time if not automatically inferred
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"  # e.g., "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The conversion process extracts available metadata from the TDT files and creates a properly formatted NWB file with the electrophysiology data.
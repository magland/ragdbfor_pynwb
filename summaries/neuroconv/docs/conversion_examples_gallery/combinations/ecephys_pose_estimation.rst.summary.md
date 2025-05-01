# Electrophysiology and Behavior in NWB

This example demonstrates how to combine electrophysiology and behavioral data (pose estimation) into an NWB file using PyNWB through the NeuroConv package.

## Data Interfaces Used
- `BlackrockRecordingInterface`: For electrophysiology recording data
- `KiloSortSortingInterface`: For spike sorting results
- `SLEAPInterface`: For pose estimation data

## Usage Example

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv import ConverterPipe
from neuroconv.datainterfaces import BlackrockRecordingInterface, KiloSortSortingInterface, SLEAPInterface

# Initialize interfaces for each data type
interface_blackrock = BlackrockRecordingInterface(file_path=file_path, verbose=False)
interface_kilosort = KiloSortSortingInterface(folder_path=folder_path, verbose=False)
interface_sleap = SLEAPInterface(file_path=file_path, verbose=False)

# Create a converter pipeline with all interfaces
converter = ConverterPipe(
    data_interfaces=[interface_blackrock, interface_kilosort, interface_sleap],
    verbose=False
)

# Extract metadata from source files
metadata = converter.get_metadata()

# Add session start time with timezone information
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific")).isoformat()
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion to create an NWB file
nwbfile_path = "path_to_save_nwbfile"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The example demonstrates how to use NeuroConv's `ConverterPipe` to coordinate the concurrent conversion of multiple data types into a single NWB file.
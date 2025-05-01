# European Data Format (EDF) Conversion

## Installation

Install NeuroConv with the necessary dependencies for EDF data:

```bash
pip install "neuroconv[edf]"
```

## Converting EDF Data to NWB Format

Use the `EDFRecordingInterface` class to convert EDF data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import EDFRecordingInterface

# Set the path to your EDF file
file_path = f"{ECEPHY_DATA_PATH}/edf/edf+C.edf"

# Initialize the interface
interface = EDFRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add time zone information for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion to NWB
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts metadata from the EDF file and creates an NWB file with the specified session start time and other parameters.
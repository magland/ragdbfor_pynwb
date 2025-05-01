# Blackrock Data Conversion to NWB

## Installation
Install NeuroConv with Blackrock-specific dependencies:
```bash
pip install "neuroconv[blackrock]"
```

## Converting Blackrock Data to NWB Format

The following example demonstrates how to convert Blackrock (.ns5) data to NWB format using the `BlackrockRecordingInterface`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import BlackrockRecordingInterface

# Path to the .ns5 file
file_path = f"{ECEPHY_DATA_PATH}/blackrock/FileSpec2.3001.ns5"

# Initialize the interface
interface = BlackrockRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"]
session_start_time = session_start_time.replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Specify output path and run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

Note: Ripple Neuro also records data in the Blackrock format, so this conversion process works for those files as well.
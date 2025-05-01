# Blackrock Sorting Data Conversion with NeuroConv

## Installation

Install NeuroConv with Blackrock dependencies:

```bash
pip install "neuroconv[blackrock]"
```

## Converting Blackrock Sorting Data to NWB

Use the `BlackrockSortingInterface` to convert Blackrock sorting data:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import BlackrockSortingInterface

file_path = f"{ECEPHY_DATA_PATH}/blackrock/FileSpec2.3001.nev"
# Change the file_path to your file location
interface = BlackrockSortingInterface(file_path=file_path, sampling_frequency=30000.0, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add time zone information for data provenance
session_start_time = datetime.fromisoformat(metadata["NWBFile"]["session_start_time"])
session_start_time = session_start_time.replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Specify output path and run conversion
nwbfile_path = f"{path_to_save_nwbfile}"  # Should be like: "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
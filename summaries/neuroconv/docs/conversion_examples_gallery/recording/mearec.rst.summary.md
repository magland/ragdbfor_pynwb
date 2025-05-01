# MEArec Conversion to NWB

## Installation

Install NeuroConv with MEArec support:

```bash
pip install "neuroconv[mearec]"
```

## Conversion Process

Use the `MEArecRecordingInterface` to convert MEArec data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import MEArecRecordingInterface

file_path = f"{ECEPHY_DATA_PATH}/mearec/mearec_test_10s.h5"
interface = MEArecRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This code demonstrates how to convert MEArec extracellular electrophysiology recordings into the NWB format using NeuroConv's dedicated interface.
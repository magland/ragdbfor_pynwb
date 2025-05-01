# Phy Sorting Data Conversion to NWB

## Installation

Install NeuroConv with Phy support:

```bash
pip install "neuroconv[phy]"
```

## Converting Phy Data to NWB

The PhySortingInterface allows conversion of Phy spike sorting data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from neuroconv.datainterfaces import PhySortingInterface

# Path to Phy data folder
folder_path = f"{ECEPHY_DATA_PATH}/phy/phy_example_0"

# Initialize interface
interface = PhySortingInterface(folder_path=folder_path, verbose=False)

# Get and update metadata
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = f"{path_to_save_nwbfile}"  # e.g., "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
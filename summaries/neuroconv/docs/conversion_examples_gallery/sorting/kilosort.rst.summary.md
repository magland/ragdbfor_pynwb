# KiloSort Data Conversion to NWB

## Installation

Install NeuroConv with KiloSort dependencies:

```bash
pip install "neuroconv[kilosort]"
```

## Converting KiloSort Data to NWB

The `KiloSortSortingInterface` can be used to convert KiloSort-processed electrophysiology data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from neuroconv.datainterfaces import KiloSortSortingInterface

folder_path = f"{ECEPHY_DATA_PATH}/phy/phy_example_0"
# Change the folder_path to the location of the data in your system
interface = KiloSortSortingInterface(folder_path=folder_path, verbose=False)

metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)
nwbfile_path = f"{path_to_save_nwbfile}"  # This should be something like: "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts spike sorting results from KiloSort output files and stores them in properly structured NWB format.
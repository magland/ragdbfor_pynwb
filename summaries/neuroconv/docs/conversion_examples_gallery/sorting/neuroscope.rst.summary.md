# NeuroScope Sorting Data Conversion to NWB

## Installation
Install NeuroConv with the neuroscope dependencies:
```bash
pip install "neuroconv[neuroscope]"
```

## Converting NeuroScope Sorting Data to NWB
Use the `NeuroScopeSortingInterface` class to convert NeuroScope sorting data:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import NeuroScopeSortingInterface

# Set paths to data
folder_path = f"{ECEPHY_DATA_PATH}/neuroscope/dataset_1"
xml_file_path = folder_path + "/YutaMouse42-151117.xml"

# Create interface with both folder_path (containing .clu and .res files) and xml_file_path
interface = NeuroScopeSortingInterface(folder_path=folder_path, xml_file_path=xml_file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Set required session_start_time if not automatically inferred
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Save as NWB file
nwbfile_path = f"{path_to_save_nwbfile}"  # e.g., "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
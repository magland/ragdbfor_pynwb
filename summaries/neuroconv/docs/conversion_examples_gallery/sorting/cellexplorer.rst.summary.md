# CellExplorer Data Conversion to NWB

This document explains how to convert CellExplorer sorting data to NWB format using NeuroConv.

## Installation

Install NeuroConv with CellExplorer dependencies:

```bash
pip install "neuroconv[cellexplorer]"
```

## Converting CellExplorer Data

Use the `CellExplorerSortingInterface` class to convert CellExplorer sorting data to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import CellExplorerSortingInterface

# Specify the path to the cellinfo.mat file
file_path = "/path/to/your/file.spikes.cellinfo.mat"

# Create the interface
interface = CellExplorerSortingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add session start time with timezone information
tzinfo = ZoneInfo("US/Pacific")
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific")).isoformat()
metadata["NWBFile"].update(session_start_time=session_start_time)

# Convert and save as NWB file
nwbfile_path = "path/to/save/file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

Note: The interface requires the location of a `cellinfo.mat` file from the CellExplorer dataset.
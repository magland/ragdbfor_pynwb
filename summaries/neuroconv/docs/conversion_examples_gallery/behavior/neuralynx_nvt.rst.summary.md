# Neuralynx NVT Data Conversion to NWB

This document explains how to convert Neuralynx NVT (position tracking) data to the NWB format using NeuroConv.

## Installation
```bash
pip install neuroconv
```

## Usage Example
```python
from datetime import datetime
from zoneinfo import ZoneInfo
from neuroconv.datainterfaces import NeuralynxNvtInterface

# Specify path to the .nvt file
file_path = "path/to/your/data/test.nvt"

# Initialize the interface
interface = NeuralynxNvtInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Add timezone information (required by NWB)
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion and save the NWB file
nwbfile_path = "path/to/save/your_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The `NeuralynxNvtInterface` class handles the conversion of position tracking data from Neuralynx's NVT format to NWB format, storing the necessary behavioral information in the resulting NWB file.
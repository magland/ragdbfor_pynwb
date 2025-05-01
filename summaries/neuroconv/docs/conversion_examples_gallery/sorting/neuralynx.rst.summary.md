# Neuralynx Data Conversion to NWB

This guide explains how to convert Neuralynx electrophysiology data to NWB format using NeuroConv.

## Installation

Install NeuroConv with Neuralynx support:

```bash
pip install "neuroconv[neuralynx]"
```

## Usage Example

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from neuroconv.datainterfaces import NeuralynxSortingInterface

# Specify the folder containing Neuralynx data
folder_path = "/path/to/neuralynx/data"

# Initialize the interface
# stream_id is optional but used to specify sampling frequency
interface = NeuralynxSortingInterface(folder_path=folder_path, verbose=False, stream_id="0")

# Get metadata and set session start time
metadata = interface.get_metadata()
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific")).isoformat()
metadata["NWBFile"].update(session_start_time=session_start_time)

# Specify output NWB file path
nwbfile_path = "/path/to/save/neuralynx_conversion.nwb"

# Run the conversion
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
# AlphaOmega Data Conversion to NWB

This guide explains how to convert AlphaOmega electrophysiology data to NWB format using NeuroConv.

## Installation

Install NeuroConv with AlphaOmega dependencies:

```bash
pip install "neuroconv[alphaomega]"
```

## Conversion Example

The following example demonstrates how to use the `AlphaOmegaRecordingInterface` to convert AlphaOmega data to NWB format:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import AlphaOmegaRecordingInterface

folder_path = f"{ECEPHY_DATA_PATH}/alphaomega/mpx_map_version4/"
# Change the file_path to the location in your system
interface = AlphaOmegaRecordingInterface(folder_path=folder_path, verbose=False)

# Extract what metadata we can from the source files
metadata = interface.get_metadata()

# Choose a path for saving the nwb file and run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts metadata automatically from the source files and creates an NWB file at the specified location.
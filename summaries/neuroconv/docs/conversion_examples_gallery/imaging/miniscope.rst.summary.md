# Miniscope Data Conversion with NeuroConv

## Installation

```bash
pip install "neuroconv[miniscope]"
```

## Overview
The `MiniscopeConverter` combines optical physiology recordings and behavioral video data from Miniscope into a single NWB file.

## Usage Example

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.converters import MiniscopeConverter

# Path to main Miniscope folder containing both recording and behavioral data streams
folder_path = str(OPHYS_DATA_PATH / "imaging_datasets" / "Miniscope" / "C6-J588_Disc5")
converter = MiniscopeConverter(folder_path=folder_path, verbose=False)

# Get metadata and add timezone information for provenance
metadata = converter.get_metadata()
session_start_time = metadata["NWBFile"]["session_start_time"]
tzinfo = ZoneInfo("US/Pacific")
metadata["NWBFile"].update(session_start_time=session_start_time.replace(tzinfo=tzinfo))

# Convert and save to NWB file
nwbfile_path = f"{path_to_save_nwbfile}"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
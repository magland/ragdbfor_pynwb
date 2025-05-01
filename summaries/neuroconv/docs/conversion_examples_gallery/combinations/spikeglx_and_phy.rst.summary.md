# SpikeGLX & Phy Integration with PyNWB

This document explains how to combine electrophysiology recordings (SpikeGLX) with spike sorting data (Phy) in a single NWB conversion using the NeuroConv library with PyNWB.

## Key Components:
- Uses `SpikeGLXRecordingInterface` for handling SpikeGLX recordings
- Uses `PhySortingInterface` for handling Phy spike sorting results
- Coordinates the concurrent conversion with `ConverterPipe`

## Example Usage:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv import ConverterPipe
from neuroconv.datainterfaces import SpikeGLXRecordingInterface, PhySortingInterface

# Define SpikeGLX interface with path to .bin file
folder_path = f"{ECEPHY_DATA_PATH}/spikeglx/Noise4Sam_g0/Noise4Sam_g0_imec0"
interface_spikeglx = SpikeGLXRecordingInterface(
    folder_path=folder_path, 
    stream_id="imec0.ap", 
    verbose=False
)

# Define Phy interface
folder_path = f"{ECEPHY_DATA_PATH}/phy/phy_example_0"
interface_phy = PhySortingInterface(folder_path=folder_path, verbose=False)

# Create converter pipe with both interfaces
converter = ConverterPipe(data_interfaces=[interface_spikeglx, interface_phy], verbose=False)

# Extract metadata from source files
metadata = converter.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion to NWB
nwbfile_path = f"{path_to_save_nwbfile}"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This workflow allows simultaneous conversion of electrophysiology recording data and spike sorting results into a single NWB file.
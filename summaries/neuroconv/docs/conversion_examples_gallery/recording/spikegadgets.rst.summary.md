# SpikeGadgets Data Conversion to NWB

## Installation
Install NeuroConv with SpikeGadgets support:
```bash
pip install "neuroconv[spikegadgets]"
```

## Conversion Process
Use the `SpikeGadgetsRecordingInterface` to convert SpikeGadgets data to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import SpikeGadgetsRecordingInterface

# Specify path to the SpikeGadgets data file
file_path = "/path/to/spikegadgets/data.rec"

# Create interface instance
interface = SpikeGadgetsRecordingInterface(file_path=file_path, verbose=False)

# Extract metadata from source files
metadata = interface.get_metadata()

# Set session start time with timezone for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run the conversion
nwbfile_path = "/path/to/save/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

This process extracts available metadata from the SpikeGadgets files and converts the recording data into the NWB format.
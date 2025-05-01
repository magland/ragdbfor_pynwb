# SpikeGLX Data Conversion to NWB

## Basic Installation

```bash
pip install "neuroconv[spikeglx]"
```

## Full SpikeGLX Dataset Conversion

The `SpikeGLXConverterPipe` allows converting all data in a SpikeGLX folder structure to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.converters import SpikeGLXConverterPipe

folder_path = f"{ECEPHY_DATA_PATH}/spikeglx/Noise4Sam_g0"
converter = SpikeGLXConverterPipe(folder_path=folder_path)

# Extract metadata from source files
metadata = converter.get_metadata()

# Add timezone information for data provenance
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Save the NWB file
nwbfile_path = output_folder / "my_spikeglx_session.nwb"
converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

## Single Stream Conversion

For converting a single band (AP or LF) on a single NeuroPixels probe:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from neuroconv.datainterfaces import SpikeGLXRecordingInterface

# Point to the .bin file location
folder_path = f"{ECEPHY_DATA_PATH}/spikeglx/Noise4Sam_g0/Noise4Sam_g0_imec0"

# Choose appropriate stream ID (e.g., "imec0.ap", "imec0.lf", "imec1.ap", "imec1.lf")
interface = SpikeGLXRecordingInterface(folder_path=folder_path, stream_id="imec0.ap", verbose=False)

# Extract metadata
metadata = interface.get_metadata()

# Add timezone information
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
nwbfile_path = f"{path_to_save_nwbfile}"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```
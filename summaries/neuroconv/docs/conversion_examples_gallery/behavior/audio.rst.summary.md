# Audio Data Conversion with NeuroConv

## Installation

Install NeuroConv with audio dependencies:

```bash
pip install "neuroconv[audio]"
```

## Converting WAV Files to NWB

The `AudioInterface` class handles WAV to NWB conversion:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from neuroconv.datainterfaces.behavior.audio.audiointerface import AudioInterface

# Path to audio file
audio_file_path = BEHAVIOR_DATA_PATH / "audio" / "natural_audio_recording.wav"

# Create interface instance
interface = AudioInterface(file_paths=[audio_file_path], verbose=False)

# Get metadata
metadata = interface.get_metadata()

# Add time zone information for data provenance
session_start_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Run conversion
interface.run_conversion(nwbfile_path=path_to_save_nwbfile, metadata=metadata)
```
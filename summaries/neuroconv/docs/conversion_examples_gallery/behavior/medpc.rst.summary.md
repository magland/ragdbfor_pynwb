# MedPC to NWB Conversion

This guide explains how to convert MedPC output files (containing operant behavior data like nose pokes and rewards) to NWB format.

## Installation

Install NeuroConv with MedPC support:

```bash
pip install neuroconv[medpc]
```

## Conversion Process

Use the `MedPCInterface` to convert MedPC output data to NWB:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from neuroconv.datainterfaces import MedPCInterface

# Path to MedPC output file
file_path = "path/to/example_medpc_file.txt"

# Session conditions to identify the session within the file
session_conditions = {"Start Date": "04/18/19", "Start Time": "10:41:42"}

# Define which variable marks the beginning of the session
start_variable = "Start Date"

# Mapping of MedPC metadata fields to internal names
metadata_medpc_name_to_info_dict = dict(
    "Start Date": {"name": "start_date", "is_array": False},
    "Start Time": {"name": "start_time", "is_array": False},
    "Subject": {"name": "subject", "is_array": False},
    "Box": {"name": "box", "is_array": False},
    "MSN": {"name": "MSN", "is_array": False},
)

# Initialize the interface
interface = MedPCInterface(
    file_path=file_path,
    session_conditions=session_conditions,
    start_variable=start_variable,
    metadata_medpc_name_to_info_dict=metadata_medpc_name_to_info_dict
)

# Extract metadata
metadata = interface.get_metadata()

# Add timezone information (required by NWB)
session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=ZoneInfo("US/Pacific"))
metadata["NWBFile"].update(session_start_time=session_start_time)

# Define mapping of MedPC variable names to behavioral events
metadata["MedPC"]["medpc_name_to_info_dict"] = {
    "A": {"name": "left_nose_poke_times", "is_array": True},
    "B": {"name": "left_reward_times", "is_array": True},
    "C": {"name": "right_nose_poke_times", "is_array": True},
    "D": {"name": "right_reward_times", "is_array": True},
    "E": {"name": "duration_of_port_entry", "is_array": True},
    "G": {"name": "port_entry_times", "is_array": True},
    "H": {"name": "footshock_times", "is_array": True},
}

# Define event descriptions
metadata["MedPC"]["Events"] = [
    {"name": "left_nose_poke_times", "description": "Left nose poke times."},
    {"name": "left_reward_times", "description": "Left reward times."},
    {"name": "right_nose_poke_times", "description": "Right nose poke times."},
    {"name": "right_reward_times", "description": "Right reward times."},
    {"name": "footshock_times", "description": "Footshock times."},
]

# Define interval series for port entries
metadata["MedPC"]["IntervalSeries"] = [
    {
        "name": "reward_port_intervals",
        "description": "Interval of time spent in reward port (1 is entry, -1 is exit).",
        "onset_name": "port_entry_times",
        "duration_name": "duration_of_port_entry",
    },
]

# Run the conversion
nwbfile_path = "path/to/output.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
```

The conversion process maps MedPC variables to behavioral events in the NWB file, allowing for proper organization of nose poke events, rewards, and other behavioral metrics.
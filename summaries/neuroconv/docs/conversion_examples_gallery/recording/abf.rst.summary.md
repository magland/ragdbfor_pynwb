# ABF Data Conversion to NWB Format

This document explains how to convert Axon Binary Format (ABF) intracellular electrophysiology data to Neurodata Without Borders (NWB) format using NeuroConv.

## Installation

Install NeuroConv with ABF support:

```bash
pip install "neuroconv[abf]"
```

## Converting Single ABF File

```python
from neuroconv.datainterfaces import AbfInterface

# Metadata info
icephys_metadata = {
    "cell_id": "20220818001",
    "slice_id": "20220818001",
    "targeted_layer": "L2-3(medial)",
    "inferred_layer": "",
    "recording_sessions": [
        {
            "abf_file_name": "File_axon_5.abf",
            "stimulus_type": "long_square",
            "icephys_experiment_type": "voltage_clamp"
        }
    ]
}

# Instantiate data interface
interface = AbfInterface(
    file_paths=[f"{ECEPHY_DATA_PATH}/axon/File_axon_5.abf"],
    icephys_metadata=icephys_metadata
)

# Get metadata from source data and modify any values you want
metadata = interface.get_metadata()
metadata['NWBFile'].update(
    identifier="ID1234",
    session_description="Intracellular electrophysiology experiment.",
    lab="my lab name",
    institution="My University",
    experimenter=["John Doe", "Jane Doe"],
)
metadata["Subject"] = dict(
    subject_id="subject_ID123",
    species="Mus musculus",
    sex="M",
    date_of_birth="2022-03-15T00:00:00"
)

# Run conversion
interface.run_conversion(nwbfile_path=output_folder / "single_abf_conversion.nwb", metadata=metadata)
```

## Converting Multiple ABF Files

For experiments with multiple ABF files (one per stimulus type):

```python
from neuroconv.datainterfaces import AbfInterface

# Metadata info
icephys_metadata = {
    "cell_id": "20220818001",
    "slice_id": "20220818001",
    "targeted_layer": "L2-3(medial)",
    "inferred_layer": "",
    "recording_sessions": [
        {
            "abf_file_name": "File_axon_5.abf",
            "stimulus_type": "long_square",
            "icephys_experiment_type": "voltage_clamp"
        },
        {
            "abf_file_name": "File_axon_6.abf",
            "stimulus_type": "short_square",
            "icephys_experiment_type": "voltage_clamp"
        }
    ]
}

# Instantiate data interface with multiple files
interface = AbfInterface(
    file_paths=[
        f"{ECEPHY_DATA_PATH}/axon/File_axon_5.abf",
        f"{ECEPHY_DATA_PATH}/axon/File_axon_6.abf",
    ],
    icephys_metadata=icephys_metadata
)

# Get and update metadata
metadata = interface.get_metadata()
metadata['NWBFile'].update(
    identifier="ID1234",
    session_description="Intracellular electrophysiology experiment.",
    lab="my lab name",
    institution="My University",
    experimenter=["John Doe", "Jane Doe"],
)
metadata["Subject"] = dict(
    subject_id="subject_ID123",
    species="Mus musculus",
    sex="M",
    date_of_birth="2022-03-15T00:00:00"
)

# Run conversion
interface.run_conversion(nwbfile_path=output_folder / "multiple_abf_conversion.nwb", metadata=metadata)
```
# PyNWB Term Validation Configuration Guide

## Overview
PyNWB allows users to validate field values against predefined sets of allowed terms using configuration files. This ensures data consistency and adherence to standards.

## Core Concepts
- **Term Validation**: Restricting field values to a set of allowed terms
- **Configuration File**: YAML file that defines validation rules
- **Term Sets**: Collections of allowed values for specific fields

## Configuration Process

### 1. Creating a Configuration File
- Use YAML syntax to define validation rules
- Specify namespaces, data types, and fields to validate
- Example: https://github.com/NeurodataWithoutBorders/pynwb/tree/dev/src/pynwb/config/nwb_config.yaml

Structure:
```yaml
namespaces:
  namespace_name:
    version: "version_number"
    data_types:
      - type_name:
          fields:
            - field_name: term_set_definition
```

### 2. Loading the Configuration
```python
from pynwb import load_type_config
load_type_config(config_path='path/to/config.yaml')
```

### 3. Using the Configuration
Once loaded, validation happens automatically when creating NWB objects:

```python
from pynwb import NWBFile
from pynwb.file import Subject
from datetime import datetime
from dateutil import tz

# Create NWB file with fields that will be validated
nwbfile = NWBFile(
    session_description="Mouse exploring an open field",
    identifier="unique_id",
    session_start_time=datetime(2018, 4, 25, 2, 30, 3, tzinfo=tz.gettz("US/Pacific")),
    experimenter=["Bilbo Baggins"]  # This will be validated if configured
)

# Create subject with fields that will be validated
subject = Subject(
    subject_id="001",
    age="P90D",
    species="Mus musculus",  # This will be validated if configured
    sex="M"
)

nwbfile.subject = subject
```

### 4. Managing Configurations
Check current configuration:
```python
from pynwb import get_loaded_type_config
config = get_loaded_type_config()
```

Unload configuration:
```python
from pynwb import unload_type_config
unload_type_config()
```

## Alternative Approach
For greater control, use `TermSetWrapper` directly on individual datasets/attributes.
See the [HDMF TermSet tutorial](https://hdmf.readthedocs.io/en/stable/tutorials/plot_term_set.html) for details.

## Dependencies
The functionality requires `linkml-runtime`. Install with:
```
pip install linkml-runtime
```
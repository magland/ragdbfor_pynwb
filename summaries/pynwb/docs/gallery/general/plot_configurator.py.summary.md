This document explains how to configure term validations in PyNWB using configuration files.

**Configuration File Structure:**

*   Uses YAML syntax.
*   Nested dictionaries define namespaces, data types, and fields with associated `TermSet`s.
*   Namespaces (e.g., core namespace, extension namespaces) and their versions must be defined.
*   Each data type has a list of fields to be validated.
*   Each field is linked to a `TermSet`, which can be unique or shared.

**Usage:**

1.  **Load the configuration file:** Use `pynwb.load_type_config(config_path='path/to/your/config.yaml')`.
2.  After loading, PyNWB will automatically wrap the fields specified in the configuration file with a `TermSetWrapper`.
3.  Example:
    ```python
    from pynwb import NWBFile, get_loaded_type_config, load_type_config, unload_type_config
    from pynwb.file import Subject
    from datetime import datetime
    from dateutil import tz
    from uuid import uuid4
    import os

    # Load the configuration
    try:
        dir_path = os.path.dirname(os.path.abspath(__file__))  # when running as a .py
    except NameError:
        dir_path = os.path.dirname(os.path.abspath("__file__"))  # when running as a script or notebook
    yaml_file = os.path.join(dir_path, 'nwb_gallery_config.yaml')
    load_type_config(config_path=yaml_file)

    session_start_time = datetime(2018, 4, 25, hour=2, minute=30, second=3, tzinfo=tz.gettz("US/Pacific"))

    # Create an NWBFile object (example assumes 'experimenter' is in the config)
    nwbfile = NWBFile(
        session_description="Mouse exploring an open field",  # required
        identifier=str(uuid4()),  # required
        session_start_time=session_start_time,  # required
        session_id="session_1234",  # optional
        experimenter=[
            "Bilbo Baggins",
        ],  # optional
        lab="Bag End Laboratory",  # optional
        institution="University of My Institution",  # optional
        experiment_description="I went on an adventure to reclaim vast treasures.",  # optional
        related_publications="DOI:10.1016/j.neuron.2016.12.011",  # optional
    )

    subject = Subject(
        subject_id="001",
        age="P90D",
        description="mouse 5",
        species="Mus musculus",
        sex="M",
    )

    nwbfile.subject = subject
    ```
4.  **View the active configuration:** Use `pynwb.get_loaded_type_config()` to retrieve the dictionary representing the current configuration.
5.  **Unload the configuration:** Use `pynwb.unload_type_config()` to stop automatic validation.

**Important Notes:**

*   When the configuration is loaded, create instances as usual; the wrapping and validation occur automatically.
*   The configuration determines which fields are validated against which sets of allowed terms.
*   The example uses `experimenter` in `NWBFile` and `species` in `Subject` as examples of fields configured for validation.

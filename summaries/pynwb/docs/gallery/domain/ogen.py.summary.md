# Optogenetics in PyNWB

## Overview
This tutorial demonstrates how to write optogenetics data using PyNWB.

## Creating an NWBFile

```python
from datetime import datetime
from uuid import uuid4
from dateutil.tz import tzlocal
from pynwb import NWBFile

nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tzlocal()),
    experimenter="Baggins, Bilbo",
    lab="Bag End Laboratory",
    institution="University of Middle Earth at the Shire",
    experiment_description="I went on an adventure to reclaim vast treasures.",
    session_id="LONELYMTN",
)
```

## Adding Optogenetic Data

The `pynwb.ogen` module contains two key data types:
- `OptogeneticStimulusSite`: Contains metadata about the stimulus site
- `OptogeneticSeries`: Contains the power applied by the laser over time (in watts)

### 1. Create a Device

```python
device = nwbfile.create_device(
    name="device",
    description="description of device",
    manufacturer="optional but recommended",
)
```

### 2. Create an OptogeneticStimulusSite

#### Method 1: Using `create_ogen_site` method
```python
ogen_site = nwbfile.create_ogen_site(
    name="OptogeneticStimulusSite",
    device=device,
    description="This is an example optogenetic site.",
    excitation_lambda=600.0,  # nm
    location="VISrl",
)
```

#### Method 2: Direct creation
```python
from pynwb.ogen import OptogeneticStimulusSite

ogen_stim_site = OptogeneticStimulusSite(
    name="OptogeneticStimulusSite2",
    device=device,
    description="This is an example optogenetic site.",
    excitation_lambda=600.0,  # nm
    location="VISrl",
)

nwbfile.add_ogen_site(ogen_stim_site)
```

The second approach is necessary when using an extension of `OptogeneticStimulusSite`.

### 3. Create an OptogeneticSeries

```python
import numpy as np
from pynwb.ogen import OptogeneticSeries

ogen_series = OptogeneticSeries(
    name="OptogeneticSeries",
    data=np.random.randn(20),  # watts
    site=ogen_site,
    rate=30.0,  # Hz
)

nwbfile.add_stimulus(ogen_series)
```

Note: By default, the starting time of the time series is the session start time specified in the NWBFile. For samples at irregular intervals, use the `timestamps` parameter instead of `rate`.
Optogenetics data can be written to an NWB file using the `pynwb.ogen` module, which includes `OptogeneticStimulusSite` for metadata about the stimulus site and `OptogeneticSeries` for the laser power applied over time.

First, create an `NWBFile` object:

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

Create a `Device` object and link it to the `NWBFile`:

```python
device = nwbfile.create_device(
    name="device",
    description="description of device",
    manufacturer="optional but recommended",
)
```

Create an `OptogeneticStimulusSite`. This can be done using `nwbfile.create_ogen_site`:

```python
ogen_site = nwbfile.create_ogen_site(
    name="OptogeneticStimulusSite",
    device=device,
    description="This is an example optogenetic site.",
    excitation_lambda=600.0,  # nm
    location="VISrl",
)
```

Alternatively, create an `OptogeneticStimulusSite` object and add it to the `NWBFile` with `nwbfile.add_ogen_site`:

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

Create an `OptogeneticSeries` and add it as a stimulus:

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

If data are sampled at irregular intervals, use the `timestamps` argument instead of `rate`.

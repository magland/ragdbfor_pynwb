# Object IDs in NWB

NWB container objects have a UUID string as an object ID, which can be accessed with the `.object_id` method. These IDs are practically unique and allow direct access to NWB objects.

## Key features

- Every NWB container object has an `object_id` (UUID string)
- The `NWBFile.objects` property provides a dictionary of all neurodata_type objects indexed by their object ID
- You can look up objects directly using their object ID

## Usage examples

```python
from datetime import datetime
import numpy as np
from dateutil.tz import tzlocal
from pynwb import NWBFile, TimeSeries

# Create NWBFile
start_time = datetime(2019, 4, 3, 11, tzinfo=tzlocal())
nwbfile = NWBFile(
    session_description="demonstrate NWB object IDs",
    identifier="NWB456",
    session_start_time=start_time,
)

# Create and add TimeSeries
timestamps = np.linspace(0, 100, 1024)
data = np.sin(0.333 * timestamps) + np.cos(0.1 * timestamps) + np.random.randn(len(timestamps))
test_ts = TimeSeries(name="raw_timeseries", data=data, unit="m", timestamps=timestamps)
nwbfile.add_acquisition(test_ts)

# Access object IDs
print(nwbfile.object_id)  # Prints UUID string
print(test_ts.object_id)  # Prints UUID string

# Access objects dictionary
print(nwbfile.objects)  # Dictionary of all objects indexed by object ID

# Iterate through objects
for oid in nwbfile.objects:
    print(nwbfile.objects[oid])

for obj in nwbfile.objects.values():
    print('%s: %s "%s"' % (obj.object_id, obj.neurodata_type, obj.name))

# Retrieve object by ID
ts_id = test_ts.object_id
my_ts = nwbfile.objects[ts_id]  # Retrieves the TimeSeries object
```

Note: Object IDs are not hash values of the data. They remain the same even if the object's contents change.
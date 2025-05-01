# Iterative Data Write in PyNWB

PyNWB supports iterative data writing, which is essential when working with large arrays or streaming data. This approach helps to avoid loading entire datasets into memory and instead writes data incrementally.

## Key Concepts

- **DataChunk**: A data structure representing a subset of a larger array, consisting of:
  - `DataChunk.data`: Contains the chunk's data values
  - `DataChunk.selection`: NumPy index tuple describing the chunk's location in the whole array

- **AbstractDataChunkIterator**: Base class for iterating over large arrays one chunk at a time

- **DataChunkIterator**: Implementation that accepts any iterable and assumes iteration over the first dimension of the array; supports buffered read

- **GenericDataChunkIterator**: Semi-abstract iterator that handles buffer region selection and compatible chunk region communication

## Use Cases

1. **Large data arrays**: Write data one subblock at a time, minimizing memory requirements
2. **Data streaming**: Save data incrementally as it arrives
3. **Data generators**: Process programmatically generated data without holding everything in memory
4. **Sparse arrays**: Reduce storage size by only writing non-zero values

## Example: Using a Generator or Streaming Data

```python
from hdmf.data_utils import DataChunkIterator
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from datetime import datetime
from dateutil.tz import tzlocal

# Define a data generator
def iter_sin(chunk_length=10, max_chunks=100):
    """Generator creating random chunks of sin values"""
    x = 0
    num_chunks = 0
    while x < 0.5 and num_chunks < max_chunks:
        val = np.asarray([sin(random() * 2 * pi) for i in range(chunk_length)])
        x = random()
        num_chunks += 1
        yield val
    return

# Wrap the generator in a DataChunkIterator
data = DataChunkIterator(data=iter_sin(10))

# Create NWB file
nwbfile = NWBFile(
    session_description="demonstrate iterative write",
    identifier="12345",
    session_start_time=datetime.now(tzlocal())
)

# Create TimeSeries with our iterator
test_ts = TimeSeries(
    name="synthetic_timeseries",
    data=data,
    unit="n/a",
    rate=1.0,
)
nwbfile.add_acquisition(test_ts)

# Write the file
with NWBHDF5IO("example.nwb", "w") as io:
    io.write(nwbfile)
```

## Example: Custom DataChunkIterator for Sparse Matrices

You can create custom iterators by implementing `AbstractDataChunkIterator`:

```python
class SparseMatrixIterator(AbstractDataChunkIterator):
    def __init__(self, shape, num_chunks, chunk_shape):
        self.shape, self.num_chunks, self.chunk_shape = shape, num_chunks, chunk_shape
        self.__chunks_created = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__chunks_created < self.num_chunks:
            data = np.random.rand(np.prod(self.chunk_shape)).reshape(self.chunk_shape)
            xmin = np.random.randint(0, int(self.shape[0]/self.chunk_shape[0]), 1)[0] * self.chunk_shape[0]
            xmax = xmin + self.chunk_shape[0]
            ymin = np.random.randint(0, int(self.shape[1]/self.chunk_shape[1]), 1)[0] * self.chunk_shape[1]
            ymax = ymin + self.chunk_shape[1]
            self.__chunks_created += 1
            return DataChunk(data=data, selection=np.s_[xmin:xmax, ymin:ymax])
        else:
            raise StopIteration

    # Other required methods...
    def recommended_chunk_shape(self):
        return self.chunk_shape

    def recommended_data_shape(self):
        return self.shape

    @property
    def dtype(self):
        return np.dtype(float)

    @property
    def maxshape(self):
        return self.shape
```

## Advanced HDF5 Storage Options

Use `H5DataIO` to control HDF5-specific options:

```python
from hdmf.backends.hdf5.h5_utils import H5DataIO

# Compression with chunking
data = H5DataIO(
    data=my_iterator,
    compression="gzip", 
    compression_opts=4,
    chunks=(100, 100),
    fillvalue=np.nan
)
```

## Working with Multi-file Data

You can create iterators that combine data from multiple files:

```python
class MultiFileArrayIterator(AbstractDataChunkIterator):
    def __init__(self, channel_files, num_steps):
        self.shape = (num_steps, len(channel_files))
        self.channel_files = channel_files
        self.num_steps = num_steps
        self.__curr_index = 0

    def __next__(self):
        if self.__curr_index < len(self.channel_files):
            newfp = np.memmap(self.channel_files[self.__curr_index], 
                              dtype="float64", mode="r", shape=(self.num_steps,))
            curr_data = newfp[:]
            i = self.__curr_index
            self.__curr_index += 1
            del newfp
            return DataChunk(data=curr_data, selection=np.s_[:, i])
        else:
            raise StopIteration
    
    # Other required methods...
```

## Alternative: Custom Dataset Writing

For more control, you can first set up the file structure and then update datasets:

```python
# Set up dataset with specific options
dataio = H5DataIO(
    shape=(0, 10),
    dtype=np.dtype("float"),
    maxshape=(None, 10),
    chunks=(131072, 2),
    compression="gzip",
    shuffle=True,
    fillvalue=np.nan,
)

# Write file and keep open
io = NWBHDF5IO("file.nwb", "w")
io.write(nwbfile)

# Resize and write data in chunks
dataio.dataset.resize((8, 10))
dataio.dataset[0:3, :] = 1
dataio.dataset[3:6, :] = 2
io.close()
```
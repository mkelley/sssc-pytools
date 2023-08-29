# sssc-pytools

An LSST Solar System Science Collaboration Python toolkit.

## API sketches

### SSSource

```python
import matplotlib.pyplot as plt
from sssc import SSSource

# get all observations of a particular object and package it into an data object
target = SSSource(6098332225018)

# alternatively, just get the data
data = SSSource.get_data(6098332225018).to_table()

# or, initialize from external data as a pandas DataFrame
target = SSSource.from_pandas(data)

# print the entire data set
print(target)

# print the first observation
print(target[0])  # SSSource with a single data row

# the first 10 observations
print(target[:10])  # SSSource with 10 data rows

# print just a column
print(target.heliocentricX)

# print a single value
print(target[0].heliocentricX)  # array of length 1

# or
print(target.heliocentricX[0])  # scalar value

# a few columns have aliases
print(target.rh)  # heliocentricDist
print(target.delta)  # topocentricDist

# a few columns can be viewed in a single attribute
print(target.r)  # heliocentric distance vector
print(target.d)  # topocentric distance vector
print(target.d.x)  # the x component of d

# the DiaSource table is joined by default
print(target.mag)
print(target.midPointMjdTai)
print(target.mid_time)  # an astropy.time.Time object

# the underlying pandas DataFrame may be accessed with the .data attribute
print(target.data)

# plot
plt.clf()
plt.errorbar(target.mid_time.mjd, target.mag, target.magErr)

# highlight r-band data
i = plt.band == "r"
plt.scatter(target.mid_time.mjd[i], target.mag[i], color="tab:red")

```

### SSObject

### MPCOrb

### Widgets

```python
from sssc.widgets import Lightcurve
from IPython.display import display

ssObjectIds = [6098332225018]
lightcurve = Lightcurve(ssObjectIds)

```

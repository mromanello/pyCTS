# pyCTS


## Status

[![PyPI version](https://badge.fury.io/py/pyCTS.svg)](https://badge.fury.io/py/pyCTS)

## Description

`pyCTS` is a minimal Python implementation of the `CTS URN` class as defined in the CTS protocol. It allows for performing basic operation on CTS URNs -- the identifiers defined and used by the [CTS protocol](http://www.homermultitext.org/hmt-doc/cite/texts/ctsoverview.html) and the [CITE architecture](http://www.homermultitext.org/hmt-doc/cite/).

The current implementation is largely a port to python of [this CTS Java implementation](https://bitbucket.org/neelsmith/cts) by Neel Smith.

(**NB:** `pyCTS` can be very convenient for basic manipulations on CTS URNs. For
advanced usage of such URNs (e.g. resolution) I recommend checking out the [MyCapytain](https://github.com/Capitains/MyCapytain/) Python library).

## Installation and Usage

Installing `pyCTS` is as easy as `pip install pyCTS`.

```python
from pyCTS import CTS_URN
urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
print(urn.work) # Returns 'tlg001'
print(urn.textgroup) # Returns 'tlg0003'
print(urn.is_range()) # False
print(urn.get_citation_depth()) # Returns 2
```

For more usage examples see the doctstring tests.

## License
The source code in this repository is licensed under the GNU General Public
License version 3 (http://www.gnu.org/licenses/gpl.html).

(c) 2018 Matteo Romanello

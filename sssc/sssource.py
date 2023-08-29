from typing import Any, Optional, Union
import numpy as np
import pandas as pd
from astropy.time import Time
from pyvo.dal.tap import TAPResults
from lsst.rsp import get_tap_service

from .exceptions import RSPConnectionError


class SSSource:
    """LSST Solar System Source data.


    Parameters
    ----------

    ssObjectId : int, optional
        Initialize from data associated with this source from the SSSource
        table.

    join_diaSource : bool, optional
        If ``True``, then associated data from the DiaSource table is also
        included.

    """

    aliases = {
        "rh": "heliocentricDist",
        "delta": "topocentricDist",
        "alpha": "phaseAngle",
    }

    def __init__(self, ssObjectId: Optional[int] = None, join_diaSource: Optional[bool] = True):
        self.data = self.get_data(ssObjectId, diaSource=join_diaSource)

    @classmethod
    def from_pandas(cls, data: pd.DataFrame):
        src = cls()
        src.data = data
        return src

    @staticmethod
    def get_data(ssObjectId: int, join_diaSource: Optional[bool] = True) -> TAPResults:
        """Retrieve data from the SSSource table.


        Parameters
        ----------

        ssObjectId : int
            Initialize from data associated with this source from the SSSource
            table.

        join_diaSource : bool, optional
            If ``True``, then associated data from the DiaSource table is also
            included.


        Returns
        -------

        data : `pyvo.dal.tap.TAPResults`

        """

        if join_diaSource:
            query = f"""
                SELECT * FROM dp03_catalogs_10Yr.SSSource as sssrc
                INNER JOIN dp03_catalogs_10Yr.DiaSource as diasrc
                ON sssrc.diaSourceId = diasrc.diaSourceId
                WHERE sssrc.ssObjectId = {ssObjectId}
            """
        else:
            query = f"""
                SELECT * FROM dp03_catalogs_10Yr.SSSource as sssrc
                WHERE sssrc.ssObjectId = {ssObjectId}
            """

        service = get_tap_service("ssotap")
        if service is None:
            raise RSPConnectionError()

        return service.search(query)

    def __getattribute__(self, name: str) -> Any:
        """If the attribute is in the data table, return that column."""
        if name in self.data:
            return np.array(self.data[name])
        elif name in self.aliases:
            return np.array(self.data[self.aliases[name]])

        return object.__getattribute__(self, name)

    def __getitem__(self, i: Union[int, slice]) -> Any:
        """Get a single row."""
        if isinstance(i, slice):
            return SSSource.from_pandas(self.data[i])
        elif isinstance(i, int):
            return SSSource.from_pandas(self.data[i:i+1])
        else:
            raise KeyError()

    @property
    def r(self):
        """Heliocentric distance vector."""
        return np.recarray([self.data["heliocentricX"], self.data["heliocentricY"], self.data["heliocentricZ"]])

    @property
    def d(self):
        """Topocentric distance vector."""
        return np.recarray([self.data["topocentricX"], self.data["topocentricY"], self.data["topocentricZ"]],
                           dtype=[("x", float), ("y", float), ("z", float)])

    @property
    def mid_time(self):
        """Observation time as a `~astropy.time.Time` object."""
        return Time(self.midPointMjdTai, format="mjd", scale="tai")

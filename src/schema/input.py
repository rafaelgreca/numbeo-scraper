from typing import List, Literal, Union, Optional

from pydantic import BaseModel

from ..core.utils import partial_model


@partial_model
class Input(BaseModel):
    """
    Input schema.
    """

    category: Union[str, List[str]] = Literal[
        "cost-of-living",
        "quality-of-life",
        "crime",
        "health-care",
        "pollution",
        "traffic",
    ]
    mode: str = Literal["country", "city"]
    years: Union[int, List[Union[int, str]]] = Literal[
        2012,
        "2012-mid",
        2013,
        "2013-mid",
        2014,
        "2014-mid",
        2015,
        "2015-mid",
        2016,
        "2016-mid",
        2017,
        "2017-mid",
        2018,
        "2018-mid",
        2019,
        "2019-mid",
        2020,
        "2020-mid",
        2021,
        "2021-mid",
        2022,
        "2022-mid",
        2023,
        "2023-mid",
        2024,
        "2024-mid",
        2025,
    ]
    regions: Optional[Union[str, List[str], None]] = Literal[
        "Africa", "America", "Asia", "Europe", "Oceania"
    ]

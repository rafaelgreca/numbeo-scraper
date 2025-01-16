from typing import List, Literal, Union, Optional

from pydantic import BaseModel

from ..core.utils import partial_model


@partial_model
class Input(BaseModel):
    """
    Input schema.
    """

    category: Union[str, List[str]] = Literal["cost-of-living"]
    mode: str = Literal["country", "city"]
    years: Union[int, List[Union[int, str]]] = Literal[2023, 2024, 2025]
    regions: Optional[Union[str, List[str], None]] = Literal[
        "Africa", "America", "Asia", "Europe", "Oceania"
    ]

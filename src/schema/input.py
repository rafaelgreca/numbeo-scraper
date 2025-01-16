from pydantic import BaseModel

from typing import List, Literal, Union

class Input(BaseModel):
    """
    Input schema.
    """

    category: Union[str, List[str]] = Literal['cost-of-living']
    mode: str = Literal['country', 'city']
    years: Union[int, List[Union[int, str]]] = Literal[2023, 2024, 2025]

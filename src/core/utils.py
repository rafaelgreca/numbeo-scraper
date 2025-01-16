from copy import deepcopy
from pathlib import Path
from typing import Dict, Optional, Type, Any, Tuple

import yaml
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    """
    Make some fields optional.

    Args:
        model (Type[BaseModel]): the Pydantic's base model class.
    """

    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
            if field_name in ["regions", "currency", "countries", "historical_items"]
        },
    )


def read_yaml_credentials_file(file_path: Path, file_name: str) -> Dict:
    """
    Reads a YAML file.

    Args:
        file_path (Path): the file's path.
        file_name (str): the file's name.

    Raises:
        error: If any error occurs when trying to read the YAML
            file, then returns the error to the user.

    Returns:
        Dict: the content of the YAML file.
    """
    path = Path.joinpath(
        file_path,
        file_name,
    )

    with open(path, "r", encoding="utf-8") as file:
        try:
            context = yaml.safe_load(file)
        except yaml.YAMLError as error:
            raise error

    return context

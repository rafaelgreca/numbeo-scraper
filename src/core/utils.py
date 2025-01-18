from copy import deepcopy
from pathlib import Path
from typing import Dict, Optional, Type, Any, Tuple

import yaml
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


REGIONS_MAPPING = {
    "Africa": "002",
    "America": "019",
    "Asia": "142",
    "Europe": "150",
    "Oceania": "009",
}

ITENS_MAPPING = {
    "Price per Square Meter to Buy Apartment Outside of Centre": 101,
    "Price per Square Meter to Buy Apartment in City Centre": 100,
    "International Primary School, Yearly for 1 Child": 228,
    "Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child": 224,
    "1 Pair of Jeans (Levis 501 Or Similar)": 60,
    "1 Pair of Men Leather Business Shoes": 66,
    "1 Pair of Nike Running Shoes (Mid-Range)": 64,
    "1 Summer Dress in a Chain Store (Zara, H&M, ...)": 62,
    "Apples (1kg)": 110,
    "Banana (1kg)": 118,
    "Beef Round (1kg) (or Equivalent Back Leg Red Meat)": 121,
    "Bottle of Wine (Mid-Range)": 14,
    "Chicken Fillets (1kg)": 19,
    "Cigarettes 20 Pack (Marlboro)": 17,
    "Domestic Beer (0.5 liter bottle)": 15,
    "Eggs (regular) (12)": 11,
    "Markets: Imported Beer (0.33 liter bottle)": 16,
    "Lettuce (1 head)": 113,
    "Loaf of Fresh White Bread (500g)": 9,
    "Local Cheese (1kg)": 12,
    "Milk (regular), (1 liter)": 8,
    "Onion (1kg)": 119,
    "Oranges (1kg)": 111,
    "Potato (1kg)": 112,
    "Rice (white), (1kg)": 115,
    "Tomato (1kg)": 116,
    "Water (1.5 liter bottle)": 13,
    "Apartment (1 bedroom) Outside of Centre": 27,
    "Apartment (1 bedroom) in City Centre": 26,
    "Apartment (3 bedrooms) Outside of Centre": 29,
    "Apartment (3 bedrooms) in City Centre": 28,
    "Cappuccino (regular)": 114,
    "Coke/Pepsi (0.33 liter bottle)": 6,
    "Domestic Beer (0.5 liter draught)": 4,
    "Restaurants: Imported Beer (0.33 liter bottle)": 5,
    "McMeal at McDonalds (or Equivalent Combo Meal)": 3,
    "Meal for 2 People, Mid-range Restaurant, Three-course": 2,
    "Meal, Inexpensive Restaurant": 1,
    "Water (0.33 liter bottle)": 7,
    "Average Monthly Net Salary (After Tax)": 105,
    "Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate": 106,
    "Cinema, International Release, 1 Seat": 44,
    "Fitness Club, Monthly Fee for 1 Adult": 40,
    "Tennis Court Rent (1 Hour on Weekend)": 42,
    "Gasoline (1 liter)": 24,
    "Monthly Pass (Regular Price)": 20,
    "One-way Ticket (Local Transport)": 18,
    "Taxi 1hour Waiting (Normal Tariff)": 109,
    "Taxi 1km (Normal Tariff)": 108,
    "Taxi Start (Normal Tariff)": 107,
    "Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)": 206,
    "Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)": 25,
    "Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment": 30,
    "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)": 33,
    "Mobile Phone Monthly Plan with Calls and 10GB+ Data": 34,
}


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
            if field_name
            in ["regions", "currency", "countries", "historical_items", "cities"]
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

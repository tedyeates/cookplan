from typing import Optional, TypedDict


class Ingredient(TypedDict):
    type: str
    name: str
    quantity: str | int | float
    units: str
    step: Optional[int]
    aisle: str


class Cookware(TypedDict):
    type: str
    name: str
    quantity: str | int | float
    step: Optional[int]
    aisle: str
    
    
class Timer(TypedDict):
    type: str
    name: Optional[str]
    quantity: str | int | float
    units: str
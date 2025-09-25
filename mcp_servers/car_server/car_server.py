from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

mcp = FastMCP("CarRentalTools", host="0.0.0.0", port=8001)

# 🔹 Input Model
class SearchCarInput(BaseModel):
    city: str = Field(..., description="City where the car will be rented")
    pickup_date: str = Field(..., description="Pickup date in YYYY-MM-DD format")
    dropoff_date: str = Field(..., description="Dropoff date in YYYY-MM-DD format")
    car_type: str = Field(..., description="Type of car (e.g., SUV, Sedan, Hatchback)")

# 🔹 Output Model
class CarInfo(BaseModel):
    car_model: str = Field(..., description="Car model name")
    company: str = Field(..., description="Rental company")
    car_type: str = Field(..., description="Car type (SUV, Sedan, etc.)")
    price_per_day: float = Field(..., description="Rental price per day in USD")
    available: bool = Field(..., description="Availability status")

class SearchCarOutput(BaseModel):
    cars: List[CarInfo] = Field(..., description="List of available cars")

# 🔹 Tool Definition
@mcp.tool()
def search_car(args: SearchCarInput) -> SearchCarOutput:
    """Search available rental cars in a given city within a date range."""

    # ❗ Normalde burada car rental API'si çağrılır.
    # Biz dummy data dönüyoruz.
    dummy_cars = [
        CarInfo(
            car_model="Toyota RAV4",
            company="Avis",
            car_type="SUV",
            price_per_day=70.0,
            available=True,
        ),
        CarInfo(
            car_model="Renault Clio",
            company="Enterprise",
            car_type="Hatchback",
            price_per_day=40.0,
            available=True,
        ),
    ]

    return SearchCarOutput(cars=dummy_cars)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

mcp = FastMCP("HotelTools", host="0.0.0.0", port=8003)

# 🔹 Input Model
class SearchHotelInput(BaseModel):
    city: str = Field(..., description="City where the hotel is located")
    check_in: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    stars: int = Field(..., description="Star rating of the hotel (1-5)")

# 🔹 Output Model
class HotelInfo(BaseModel):
    hotel_name: str = Field(..., description="Hotel name")
    address: str = Field(..., description="Hotel address")
    stars: int = Field(..., description="Star rating of the hotel")
    price_per_night: float = Field(..., description="Price per night in USD")
    available_rooms: int = Field(..., description="Number of available rooms")

class SearchHotelOutput(BaseModel):
    hotels: List[HotelInfo] = Field(..., description="List of available hotels")

# 🔹 Tool Definition
@mcp.tool()
def search_hotel(args: SearchHotelInput) -> SearchHotelOutput:
    """Search for available hotels in a given city within a date range."""

    # ❗ Normalde burada otel API'si çağrılır.
    # Şimdilik dummy data dönelim.
    dummy_hotels = [
        HotelInfo(
            hotel_name="Hilton Istanbul Bosphorus",
            address="Harbiye, Istanbul",
            stars=5,
            price_per_night=250.0,
            available_rooms=8,
        ),
        HotelInfo(
            hotel_name="Dedeman Ankara",
            address="Çankaya, Ankara",
            stars=4,
            price_per_night=120.0,
            available_rooms=15,
        ),
    ]

    return SearchHotelOutput(hotels=dummy_hotels)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

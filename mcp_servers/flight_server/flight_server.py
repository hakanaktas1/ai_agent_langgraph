from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

mcp = FastMCP("FlightTools", host="0.0.0.0", port=8002)

# Input Model
class SearchFlightInput(BaseModel):
    origin: str = Field(..., description="Origin city or airport code")
    destination: str = Field(..., description="Destination city or airport code")
    date: str = Field(..., description="Flight date in YYYY-MM-DD format")

# Output Model
class FlightInfo(BaseModel):
    flight_number: str = Field(..., description="Flight number")
    airline: str = Field(..., description="Airline name")
    departure_time: str = Field(..., description="Departure time in HH:MM format")
    arrival_time: str = Field(..., description="Arrival time in HH:MM format")
    price: float = Field(..., description="Ticket price in USD")

class SearchFlightOutput(BaseModel):
    flights: List[FlightInfo] = Field(..., description="List of available flights")

# Tool Definition
@mcp.tool()
def search_flight(args: SearchFlightInput) -> SearchFlightOutput:
    """Search available flights between two cities on a given date."""
    # Burada normalde gerçek API çağrısı yapılır.
    dummy_flights = [
        FlightInfo(
            flight_number="TK123",
            airline="Turkish Airlines",
            departure_time="08:00",
            arrival_time="10:30",
            price=120.50,
        ),
        FlightInfo(
            flight_number="PC456",
            airline="Pegasus Airlines",
            departure_time="12:00",
            arrival_time="14:20",
            price=95.00,
        ),
    ]

    return SearchFlightOutput(flights=dummy_flights)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

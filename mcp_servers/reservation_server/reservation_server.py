from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("ReservationTools", host="0.0.0.0", port=8004)

class CreateReservationInput(BaseModel):
    user_id: str = Field(..., description="The user making the reservation")
    details: str = Field(..., description="Reservation details like hotel/flight info")

class ReservationResult(BaseModel):
    reservation_id: str
    status: str

@mcp.tool()
def create_reservation(args: CreateReservationInput) -> ReservationResult:
    """Create a new reservation for a user with given details."""
    # dummy result
    return ReservationResult(
        reservation_id="RSV12345",
        status=f"Reservation created for user {args.user_id}"
    )


class CancelReservationInput(BaseModel):
    reservation_id: str = Field(..., description="Reservation ID to cancel")

class CancelResult(BaseModel):
    reservation_id: str
    status: str

@mcp.tool()
def cancel_reservation(args: CancelReservationInput) -> CancelResult:
    """Cancel a reservation by ID."""
    return CancelResult(
        reservation_id=args.reservation_id,
        status="Cancelled successfully"
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

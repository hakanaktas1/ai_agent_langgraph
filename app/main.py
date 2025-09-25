import asyncio
from langgraph.graph import StateGraph, END
from state import TravelState
from supervisor.supervisor_node import supervisor_node
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.car_agent import CarAgent
from agents.reservation_agent import ReservationAgent
from agents.general_agent import GeneralAgent
from tools.mcp_adapters import init_tools

async def run():
    # MCP serverlardan tool bilgilerini al
    await init_tools()

    # StateGraph olustur
    graph = StateGraph(TravelState)

    # Node'lar
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("flight_agent", FlightAgent())
    graph.add_node("hotel_agent", HotelAgent())
    graph.add_node("car_agent", CarAgent())
    graph.add_node("reservation_agent", ReservationAgent())
    graph.add_node("general_agent", GeneralAgent())

    # Entry point
    graph.set_entry_point("supervisor")

    # Supervisor'dan domain agent'lara
    graph.add_edge("supervisor", "flight_agent")
    graph.add_edge("supervisor", "hotel_agent")
    graph.add_edge("supervisor", "car_agent")
    graph.add_edge("supervisor", "reservation_agent")
    graph.add_edge("supervisor", "general_agent")

    # Domain agent'tan tekrar supervisor'a (slot doldurma icin)
    graph.add_edge("flight_agent", "supervisor")
    graph.add_edge("hotel_agent", "supervisor")
    graph.add_edge("car_agent", "supervisor")
    graph.add_edge("reservation_agent", "supervisor")

    # Final cikislar
    graph.add_edge("flight_agent", END)
    graph.add_edge("hotel_agent", END)
    graph.add_edge("car_agent", END)
    graph.add_edge("reservation_agent", END)
    graph.add_edge("general_agent", END)

    travel_graph = graph.compile()

    print("✈️🚗🏨 Travel Asistan basladi. Cikmak icin 'exit' yaz.")
    while True:
        q = input("\nKullanici: ")
        if q.lower() in ["exit", "quit", "q"]:
            print("Asistan: Gorusuruz! 👋")
            break

        state = {
            "user_input": q,
            "results": {},
            "missing_slots": {},
            "filled_slots": {}
        }
        result = await travel_graph.ainvoke(state)

        # Domain bazli cevaplari yazdir
        if result.get("results"):
            for domain, answer in result["results"].items():
                print(f"Asistan ({domain}): {answer}")
        else:
            print("Asistan: Uygun sonuc bulunamadi.")

if __name__ == "__main__":
    asyncio.run(run())

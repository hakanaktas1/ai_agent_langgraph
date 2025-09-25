from state import TravelState
from tools.mcp_adapters import get_mcp_tool
from tools.validators import validate_slots
from models import llm
from langchain.prompts import ChatPromptTemplate
import json

class CarAgent:
    def __init__(self, model=None):
        self.llm = model or llm

    def naturalize_result(self, raw_result: dict) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Sen travel asistani olarak kullaniciya araba kiralama sonucunu anlatacaksin."),
            ("user", f"Tool ciktisi: {json.dumps(raw_result)}\nDogal bir cumle yaz.")
        ])
        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content

    def __call__(self, state: TravelState) -> TravelState:
        cars = [i for i in state["intents"] if i["domain"] == "car"]
        for intent in cars:
            tool = get_mcp_tool("car", intent["intent"])
            slots = {**intent["slots"], **state.get("filled_slots", {})}

            missing = validate_slots(tool, slots)
            if missing:
                state["missing_slots"] = {"car": missing}
                return state

            result = tool.invoke(slots)
            state["results"]["car"] = self.naturalize_result(result)
            state["missing_slots"] = {}
        return state

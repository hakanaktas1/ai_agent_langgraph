from .intent_parser import intent_parser
from state import TravelState
from models import llm
from langchain.prompts import ChatPromptTemplate

def supervisor_node(state: TravelState) -> TravelState:
    if "intents" not in state or not state["intents"]:
        intents = intent_parser(state["user_input"])
        if intents:
            state["intents"] = intents
        else:
            # intent yok → GeneralAgent'a yonlendir
            state["intents"] = [{"domain": "general", "intent": "chitchat", "slots": {}}]

    if state.get("missing_slots"):
        domain, slots = list(state["missing_slots"].items())[0]
        slot_name = slots[0]

        # Daha dogal soru icin LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Sen travel asistani olarak eksik bilgiyi kibarca soracaksin."),
            ("user", f"Kullanicidan {domain} domaini icin '{slot_name}' bilgisini iste. Kisa, dogal bir soru yaz.")
        ])
        chain = prompt | llm
        response = chain.invoke({})

        state["user_input"] = response.content
    return state

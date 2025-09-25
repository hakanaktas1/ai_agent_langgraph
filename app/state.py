from typing import TypedDict, Dict, Any, List

class TravelState(TypedDict):
    user_input: str
    intents: List[Dict[str, Any]]
    results: Dict[str, Any]
    missing_slots: Dict[str, List[str]]
    filled_slots: Dict[str, Any]

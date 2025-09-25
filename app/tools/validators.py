from typing import Dict, List

def validate_slots(tool, provided_slots: Dict) -> List[str]:
    """Pydantic input semasina gore eksik alanlari kontrol eder."""
    missing = []
    input_model = tool.input_model
    required_fields = [
        name for name, field in input_model.model_fields.items() if field.is_required()
    ]
    for field in required_fields:
        if field not in provided_slots or provided_slots[field] in [None, ""]:
            missing.append(field)
    return missing

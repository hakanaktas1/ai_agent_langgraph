import asyncio
from mcp.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "flight": {"url": "http://localhost:8002/mcp", "transport": "streamable_http"},
        "hotel": {"url": "http://localhost:8003/mcp", "transport": "streamable_http"},
        "car": {"url": "http://localhost:8001/mcp", "transport": "streamable_http"},
        "reservation": {"url": "http://localhost:8004/mcp", "transport": "streamable_http"},
    }
)

_tools_cache = {}

async def init_tools():
    """Tum MCP serverlardan tool semalarini cache'e alir."""
    global _tools_cache
    _tools_cache = await client.get_tools()
    return _tools_cache

def get_mcp_tool(domain: str, intent: str):
    if domain not in _tools_cache:
        raise ValueError(f"{domain} icin tool bulunamadi. init_tools() cagirildi mi?")

    domain_tools = _tools_cache[domain]
    for tool in domain_tools:
        if tool.name == intent:
            return tool
    raise ValueError(f"{domain} icinde {intent} intent bulunamadi.")

def build_tool_schema_prompt() -> str:
    """LLM'e verilecek tool semasi aciklamasini string olarak dondurur."""
    prompt = "Kullanabilecegin domainler ve fonksiyonlar:\n\n"
    for domain, tools in _tools_cache.items():
        prompt += f"[{domain.upper()}]\n"
        for tool in tools:
            fields = ", ".join(tool.input_model.model_fields.keys())
            prompt += f"- {tool.name}({fields})\n"
        prompt += "\n"
    return prompt

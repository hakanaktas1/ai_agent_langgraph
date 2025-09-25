import json
from models import llm
from langchain.prompts import ChatPromptTemplate
from tools.mcp_adapters import build_tool_schema_prompt

def intent_parser(user_query: str):
    schema_prompt = build_tool_schema_prompt()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen bir travel booking asistani olarak calisiyorsun."),
        ("system", f"Kullanabilecegin tool semalari:\n{schema_prompt}"),
        ("user", f"""
        Kullanici sorusu: {user_query}

        Asagidaki JSON formatinda intentleri ve slotlari cikar:

        {{
          "intents": [
            {{
              "domain": "...",
              "intent": "...",
              "slots": {{...}}
            }}
          ]
        }}

        Lutfen sadece gecerli JSON dondur.
        """)
    ])

    
    chain = prompt | llm
    response = chain.invoke({})

    try:
        parsed = json.loads(response.content)
        return parsed.get("intents", [])
    except Exception as e:
        print("Intent parse hatasi:", e, response.content)
        return []

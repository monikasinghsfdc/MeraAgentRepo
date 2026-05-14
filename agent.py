"""
Smart Config-Driven Agent
Sirf master_config.json badlo — yeh file kabhi nahi badalti!
"""

import json
from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from universal_tools import get_tools_for_industry

# ─── Config padho ────────────────────────────────────────────────────────────
with open("master_config.json") as f:
    CONFIG = json.load(f)

# Active industry config lo
ACTIVE = CONFIG["active_industry"]           # e.g. "nonprofit"
IND    = CONFIG["industries"][ACTIVE]        # us industry ka config
LLM_C  = CONFIG["llm"]                       # LLM settings

print(f"\n✅ Agent start ho raha hai: {IND['name']}")
print(f"🤖 LLM: {LLM_C['provider']} / {LLM_C['model']}\n")

# ─── LLM — config se automatic ───────────────────────────────────────────────
provider = LLM_C["provider"]

if provider == "ollama":
    llm = ChatOllama(model=LLM_C["model"], temperature=LLM_C["temperature"])

elif provider == "anthropic":
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(model=LLM_C["options"]["anthropic"]["model"])

elif provider == "openai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=LLM_C["options"]["openai"]["model"])

elif provider == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model=LLM_C["options"]["gemini"]["model"])

# ─── Tools — config se automatic ─────────────────────────────────────────────
tools = get_tools_for_industry(IND["tools"])

# ─── Prompt — config se automatic ────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", IND["system_prompt"]),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# ─── Agent banao ─────────────────────────────────────────────────────────────
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

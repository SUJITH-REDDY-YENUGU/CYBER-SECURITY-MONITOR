from langchain_core.messages import HumanMessage

async def threat_analyst(state, llm, prompt_template: str):
    prompt = prompt_template.format(
        events="\n".join(state["mapped_events"])
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"analysis": response.content}

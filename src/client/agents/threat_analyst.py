from langchain_core.messages import HumanMessage

async def threat_analyst(state, llm, prompt_template: str):
    prompt = prompt_template.format(
        events="\n".join(state["mapped_events"])
    )

    # Human-in-the-loop: allow user to add notes/feedback to steer analysis
    user_notes = state.get("user_notes")
    if user_notes:
        prompt += f"\n\n[User notes]\n{user_notes}\n"

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"analysis": response.content}

from langgraph.graph import StateGraph, START, END
from llm_parser import parse_meeting_prompt
from calendar_utils import create_meeting

# ✅ Make sure this is used as state
class SchedulerState(dict): pass

def handle_input(state):
    print("📥 handle_input received:", state)
    if "user_input" not in state:
        raise ValueError("Missing 'user_input' in state")
    state["raw_input"] = state["user_input"]
    return state

def parse_input(state):
    print("🧠 parse_input received:", state)
    parsed = parse_meeting_prompt(state["raw_input"])
    state["meeting_info"] = parsed
    return state

# def schedule_event(state):
#     print("📅 schedule_event received:", state)
#     result = create_meeting(state["meeting_info"])
#     state["event_confirmation"] = result.get("htmlLink", "Meeting scheduled!")
#     return state

def schedule_event(state):
    info = state.get("meeting_info", {})

    if "follow_up" in info:
        state["meeting_info"] = {"follow_up": info["follow_up"]}
        return state

    if not all(k in info for k in ("date", "time", "title", "duration")):
        raise ValueError("❌ Incomplete info. Please include all required fields.")

    # Proceed to schedule
    result = create_meeting(info)
    state["event_confirmation"] = result.get("htmlLink", "Meeting scheduled!")
    return state


def build_graph():
    graph = StateGraph(dict)  # ✅ USE SchedulerState HERE

    graph.add_node("input_handler", handle_input)
    graph.add_node("parser", parse_input)
    graph.add_node("scheduler", schedule_event)

    graph.add_edge(START, "input_handler")
    graph.add_edge("input_handler", "parser")
    graph.add_edge("parser", "scheduler")
    graph.add_edge("scheduler", END)

    return graph.compile()

import streamlit as st
from langgraph_scheduler import build_graph

st.title("📅 Agentic Meeting Scheduler")

# Initialize scheduler once
if "scheduler" not in st.session_state:
    st.session_state.scheduler = build_graph()

# --- Initial prompt ---
user_input = st.text_input("🗣️ Enter your meeting request:", key="initial_input")

# --- First scheduler call ---
if st.button("Schedule Meeting"):
    if not user_input.strip():
        st.warning("Please enter a meeting request.")
    else:
        result = st.session_state.scheduler.invoke(input={"user_input": user_input.strip()})

        # Success Case
        if "event_confirmation" in result:
            st.success("✅ Meeting Scheduled Successfully!")
            st.markdown(f"[📍 View it in Calendar]({result['event_confirmation']})")

        # Assistant needs follow-up
        elif "meeting_info" in result and "follow_up" in result["meeting_info"]:
            st.session_state.follow_up_prompt = result["meeting_info"]["follow_up"]
            st.session_state.pending = True
            st.rerun()

# --- Follow-up Phase ---
if st.session_state.get("pending"):
    st.info(f"🗨️ Assistant: {st.session_state.follow_up_prompt}")
    follow_up_input = st.text_input("Your reply to the assistant:", key="follow_up_input")

    if follow_up_input:
        follow_up_result = st.session_state.scheduler.invoke(input={"user_input": follow_up_input.strip()})

        if "event_confirmation" in follow_up_result:
            st.success("✅ Meeting Scheduled Successfully!")
            st.markdown(f"[📍 View it in Calendar]({follow_up_result['event_confirmation']})")
            st.session_state.pending = False

        elif "meeting_info" in follow_up_result and "follow_up" in follow_up_result["meeting_info"]:
            # Store the next follow-up message
            st.session_state.follow_up_prompt = follow_up_result["meeting_info"]["follow_up"]
            st.rerun()
        else:
            st.warning("⚠️ Still missing some information. Try rephrasing.")

import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Chat Assistant", layout="wide", page_icon="🤖")
st.title("🤖 AI Assistant with Token Tracking")

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

with st.sidebar:
    st.header("Settings")
    if st.button("🆕 Start New Chat"):
        try:
            res = requests.post(f"{BASE_URL}/sessions")
            if res.status_code == 200:
                st.session_state.current_session_id = res.json()["id"]
                st.success("New session started!")
                st.rerun()
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")

    if st.session_state.current_session_id:
        st.write(f"**Current Session:**")
        st.code(st.session_state.current_session_id)
        
        try:
            session_res = requests.get(f"{BASE_URL}/sessions/{st.session_state.current_session_id}")
            if session_res.status_code == 200:
                total_cost = session_res.json()["total_cost"]
                st.metric("Total Session Cost", f"${total_cost:.6f}")
        except:
            pass

if st.session_state.current_session_id:
    try:
        chat_res = requests.get(f"{BASE_URL}/sessions/{st.session_state.current_session_id}")
        if chat_res.status_code == 200:
            history = chat_res.json()["messages"]
            for msg in history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg["role"] == "assistant":
                        st.caption(f"Cost: ${msg['cost']:.6f} | Tokens: {msg['tokens']}")
    except Exception as e:
        st.error(f"Could not load history: {e}")

    user_input = st.chat_input("Write your message here...")
    if user_input:
        with st.spinner("AI is thinking..."):
            try:
                payload = {"user_input": user_input}
                res = requests.post(
                    f"{BASE_URL}/sessions/{st.session_state.current_session_id}/message/",
                    json=payload
                )
                
                if res.status_code == 200:
                    st.rerun()
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
else:
    st.info("Please start a new session from the sidebar to begin.")
import streamlit as st


DEMO_MESSAGES = [
    "Urgent language is a common social engineering tactic.",
    "Unexpected attachments and links should be treated carefully.",
    "Real services should not ask for your PIN, OTP, or password in chat.",
    "Safe habit: verify the sender and open the service directly from a trusted URL.",
]


def render_awareness_demo() -> None:
    st.subheader("Safe Awareness Demo")
    st.caption("This simulation runs only inside the app and does not modify files or execute anything outside Streamlit.")

    if "awareness_running" not in st.session_state:
        st.session_state.awareness_running = False

    col1, col2 = st.columns(2)
    if col1.button("Run Safe Awareness Demo", use_container_width=True):
        st.session_state.awareness_running = True
    if col2.button("Stop Demo", use_container_width=True):
        st.session_state.awareness_running = False

    if not st.session_state.awareness_running:
        st.info("Start the demo to see harmless in-app examples of scareware-style pressure tactics.")
        return

    for message in DEMO_MESSAGES:
        st.warning(message)

    st.success("This was a safe simulation. No files, browser windows, emails, or system settings were changed.")


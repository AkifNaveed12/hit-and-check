import streamlit as st


DEMO_MESSAGES = [
    {
        "icon": "🚨",
        "title": "Urgency Tactics",
        "body": "Urgent language is a common social engineering tactic used to pressure victims into acting without thinking.",
    },
    {
        "icon": "📎",
        "title": "Suspicious Attachments & Links",
        "body": "Unexpected attachments and links should always be treated with caution — even if they appear to come from someone you know.",
    },
    {
        "icon": "🔑",
        "title": "PIN / OTP Requests",
        "body": "Real services will never ask for your PIN, OTP, or password through chat messages, emails, or phone calls.",
    },
    {
        "icon": "✅",
        "title": "Safe Verification Habit",
        "body": "Always verify the sender's identity and access the service directly through a trusted, bookmarked URL rather than clicking links.",
    },
]


def render_awareness_demo() -> None:
    st.markdown("""
    <div style="margin-bottom: 4px;">
        <div style="font-size:1rem;font-weight:700;color:#94a3b8;letter-spacing:0.08em;
                    text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-bottom:14px;">
            🎓 Awareness Demo
            <span style="flex:1;height:1px;background:linear-gradient(90deg,rgba(0,212,255,0.2),transparent);display:inline-block;"></span>
        </div>
    </div>
    <p style="font-size:0.85rem;color:#475569;margin-bottom:20px;">
        This simulation runs only inside the app and does not modify files or execute anything outside Streamlit.
    </p>
    """, unsafe_allow_html=True)

    if "awareness_running" not in st.session_state:
        st.session_state.awareness_running = False

    col1, col2 = st.columns(2)
    if col1.button("▶  Run Safe Awareness Demo", use_container_width=True):
        st.session_state.awareness_running = True
    if col2.button("⏹  Stop Demo", use_container_width=True):
        st.session_state.awareness_running = False

    if not st.session_state.awareness_running:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px;color:#334155;">
            <div style="font-size:3rem;margin-bottom:12px;">🛡️</div>
            <p style="color:#475569;font-size:0.875rem;">
                Start the demo to see harmless in-app examples of scareware-style pressure tactics.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    for msg in DEMO_MESSAGES:
        st.markdown(f"""
        <div style="background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.25);
                    border-left:4px solid #fbbf24;border-radius:10px;
                    padding:16px 20px;margin-bottom:14px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="font-size:1.3rem;">{msg['icon']}</span>
                <strong style="color:#fbbf24;font-size:0.9rem;">{msg['title']}</strong>
            </div>
            <p style="margin:0;color:#cbd5e1;font-size:0.85rem;line-height:1.55;">{msg['body']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.25);
                border-left:4px solid #34d399;border-radius:10px;padding:16px 20px;margin-top:6px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.3rem;">✅</span>
            <strong style="color:#34d399;font-size:0.9rem;">Safe Simulation Complete</strong>
        </div>
        <p style="margin:6px 0 0 0;color:#cbd5e1;font-size:0.85rem;">
            No files, browser windows, emails, or system settings were changed during this demo.
        </p>
    </div>
    """, unsafe_allow_html=True)

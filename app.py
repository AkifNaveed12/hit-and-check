import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.attacks import run_attack
from src.awareness_demo import render_awareness_demo
from src.config import APP_NAME, ATTACK_TYPES, ENCRYPTION_METHODS, get_settings
from src.email_service import send_report_email
from src.encryption import transform_pin
from src.groq_client import generate_chat_response, generate_pin_report
from src.report_builder import build_chat_payload, build_email_report, build_report_payload
from src.scoring import build_score_result
from src.validators import validate_email, validate_pin


st.set_page_config(page_title=APP_NAME, page_icon="H&C", layout="wide")


def initialize_state() -> None:
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "ai_report" not in st.session_state:
        st.session_state.ai_report = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []


def render_sidebar() -> dict | None:
    st.sidebar.title(APP_NAME)
    st.sidebar.caption("Cybersecurity awareness simulator for 4-digit demo PINs.")

    with st.sidebar.form("analysis_form"):
        user_name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Optional unless sending report")
        pin = st.text_input("Demo PIN", type="password", max_chars=4, placeholder="4 digits")
        method = st.selectbox("Transformation", ENCRYPTION_METHODS)
        attack_type = st.selectbox("Attack Type", ATTACK_TYPES)
        acknowledged = st.checkbox("I confirm this is not my real ATM or banking PIN.")
        submitted = st.form_submit_button("Run Analysis", use_container_width=True)

    if not submitted:
        return None

    pin_error = validate_pin(pin)
    email_error = validate_email(email, required=False)

    if pin_error:
        st.sidebar.error(pin_error)
        return None
    if email_error:
        st.sidebar.error(email_error)
        return None
    if not acknowledged:
        st.sidebar.error("Please confirm you are using a demo PIN only.")
        return None

    return {
        "user_name": user_name.strip() or "Demo User",
        "email": email.strip(),
        "pin": pin,
        "method": method,
        "attack_type": attack_type,
    }


def run_analysis(form_data: dict) -> None:
    encrypted_pin = transform_pin(form_data["pin"], form_data["method"])
    attack_result = run_attack(encrypted_pin, form_data["method"], form_data["attack_type"])
    score_result = build_score_result(attack_result)

    st.session_state.analysis = {
        "user": {
            "name": form_data["user_name"],
            "email": form_data["email"],
        },
        "pin_data": {
            "encrypted_pin": encrypted_pin,
            "encryption_method": form_data["method"],
        },
        "attack_result": attack_result,
        "score_result": score_result,
    }
    st.session_state.ai_report = None


def render_dashboard() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.info("Enter a demo PIN in the sidebar and run the analysis.")
        return

    attack = analysis["attack_result"]
    score = analysis["score_result"]
    pin_data = analysis["pin_data"]

    st.subheader("Dashboard")
    st.caption("Educational simulation results. The original demo PIN is not shown here.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Attempts", f"{attack['attempts_to_crack']:,}")
    col2.metric("Strength Score", f"{score['strength_score_out_of_100']}/100")
    col3.metric("Hack Probability", f"{score['hack_probability_out_of_100']}%")
    col4.metric("Risk Level", score["risk_level"])

    st.write("Transformed demo PIN:", f"`{pin_data['encrypted_pin']}`")
    st.write("Transformation:", pin_data["encryption_method"])
    st.write("Attack Type:", attack["attack_type"])
    st.write("Estimated crack time:", score["estimated_crack_time_label"])

    st.progress(min(attack["crack_position_percentage"] / 100, 1.0))

    chart_data = {
        "Metric": ["Attempts Used", "Remaining Search Space"],
        "Count": [
            attack["attempts_to_crack"],
            max(attack["total_possible_combinations"] - attack["attempts_to_crack"], 0),
        ],
    }
    st.bar_chart(chart_data, x="Metric", y="Count")


def render_ai_report() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.info("Run an analysis first.")
        return

    if st.button("Generate AI Report", use_container_width=True):
        payload = build_report_payload(analysis)
        st.session_state.ai_report = generate_pin_report(payload)

    report = st.session_state.ai_report
    if not report:
        st.info("Generate the AI report to view detailed guidance.")
        return

    # Extract data with fallbacks
    risk_level = str(report.get("risk_level", "Unknown")).upper()
    summary = report.get("summary", "No summary available.")
    
    # Parse scores, fallback to 0 if missing or invalid
    try:
        strength_score = int(report.get("strength_score", 0))
    except (ValueError, TypeError):
        strength_score = 0
        
    try:
        hack_prob = int(report.get("hack_probability", 0))
    except (ValueError, TypeError):
        hack_prob = 0

    attack_explanation = report.get("attack_explanation", "")
    key_findings = report.get("key_findings", [])
    recommendations = report.get("recommendations", [])

    # Dynamic styling based on risk level
    risk_color = "#888888" # default gray
    if "HIGH" in risk_level or "CRITICAL" in risk_level:
        risk_color = "#ff4b4b" # red
    elif "MEDIUM" in risk_level:
        risk_color = "#ffa421" # orange
    elif "LOW" in risk_level:
        risk_color = "#00c04b" # green

    # Attractive Header Banner
    st.markdown(f"""
        <div style="background-color: {risk_color}15; padding: 20px; border-radius: 12px; border-left: 6px solid {risk_color}; margin-bottom: 25px;">
            <h2 style="color: {risk_color}; margin-top: 0; margin-bottom: 10px;">🛡️ AI Security Report: {risk_level} RISK</h2>
            <p style="font-size: 16px; margin: 0; color: #ececed;">{summary}</p>
        </div>
    """, unsafe_allow_html=True)

    # 2-column layout for visual gauges
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge Chart for Strength Score
        fig_strength = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = strength_score,
            title = {'text': "PIN Strength Score", 'font': {'size': 22}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#1f77b4"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': '#ff4b4b'},
                    {'range': [40, 70], 'color': '#ffa421'},
                    {'range': [70, 100], 'color': '#00c04b'}],
            }
        ))
        fig_strength.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig_strength, use_container_width=True)

    with col2:
        # Gauge Chart for Hack Probability
        fig_hack = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = hack_prob,
            title = {'text': "Hack Probability (%)", 'font': {'size': 22}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#d62728"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#00c04b'},
                    {'range': [30, 70], 'color': '#ffa421'},
                    {'range': [70, 100], 'color': '#ff4b4b'}],
            }
        ))
        fig_hack.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig_hack, use_container_width=True)

    st.markdown("---")

    # Explanation Section
    st.markdown("### 🔍 Attack Explanation")
    st.info(attack_explanation, icon="💡")

    st.markdown("---")

    # Findings and Recommendations in tables side-by-side
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### ⚠️ Key Findings")
        if key_findings:
            df_findings = pd.DataFrame({"Findings": key_findings})
            st.dataframe(df_findings, use_container_width=True, hide_index=True)
        else:
            st.info("No key findings reported.")

    with col4:
        st.markdown("### 🛡️ Recommendations")
        if recommendations:
            df_rec = pd.DataFrame({"Actionable Recommendations": recommendations})
            st.dataframe(df_rec, use_container_width=True, hide_index=True)
        else:
            st.info("No recommendations reported.")

    st.markdown("---")
    
    with st.expander("Show Raw AI Analysis JSON"):
        st.json(report)


def render_chatbot() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.info("Run an analysis first so the assistant has context.")
        return

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask about PIN safety, brute force, phishing, or better habits")
    if not prompt:
        return

    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = build_chat_payload(prompt, analysis)
    response = generate_chat_response(payload)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)


def render_email_tab() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.info("Run an analysis first.")
        return

    settings = get_settings()
    current_email = analysis["user"].get("email", "")
    email = st.text_input("Recipient Email", value=current_email)

    if st.button("Get Report on Email", use_container_width=True):
        email_error = validate_email(email, required=True)
        if email_error:
            st.error(email_error)
            return

        report = st.session_state.ai_report or generate_pin_report(build_report_payload(analysis))
        email_report = build_email_report(analysis, report)
        result = send_report_email(email, email_report, settings)
        if result["ok"]:
            st.success("Report email sent.")
        else:
            st.error(result["message"])


def main() -> None:
    initialize_state()
    form_data = render_sidebar()
    if form_data:
        run_analysis(form_data)

    st.title(APP_NAME)
    st.warning("Use a demo PIN only. Do not enter a real ATM, banking, account, or recovery PIN.")

    tabs = st.tabs(["Dashboard", "AI Report", "Security Assistant", "Email Report", "Awareness Demo"])
    with tabs[0]:
        render_dashboard()
    with tabs[1]:
        render_ai_report()
    with tabs[2]:
        render_chatbot()
    with tabs[3]:
        render_email_tab()
    with tabs[4]:
        render_awareness_demo()


if __name__ == "__main__":
    main()

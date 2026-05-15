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


st.set_page_config(page_title=APP_NAME, page_icon="🔐", layout="wide")


# ─── Global CSS ──────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #060b18 0%, #0a1628 40%, #061624 100%);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(0,212,255,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: -60%;
        right: -5%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(99,102,241,0.07) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        margin: 0;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        color: #00d4ff;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 14px;
    }

    /* ── Warning Banner ── */
    .warning-banner {
        background: linear-gradient(90deg, rgba(245,158,11,0.08), rgba(245,158,11,0.04));
        border: 1px solid rgba(245,158,11,0.3);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 24px;
        color: #fbbf24;
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(145deg, #0d1526, #111827);
        border: 1px solid rgba(0, 212, 255, 0.12);
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
        transition: border-color 0.3s, box-shadow 0.3s;
        height: 100%;
    }
    .metric-card:hover {
        border-color: rgba(0, 212, 255, 0.35);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.08);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00d4ff;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    .metric-value.red   { color: #f87171; }
    .metric-value.amber { color: #fbbf24; }
    .metric-value.green { color: #34d399; }

    /* ── Info rows ── */
    .info-grid {
        background: #0d1526;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 18px 0;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px 30px;
    }
    .info-item { }
    .info-key {
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #475569;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .info-val {
        font-size: 0.92rem;
        color: #cbd5e1;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }

    /* ── Glowing Progress Bar ── */
    .progress-wrap {
        background: #0d1526;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 18px 0;
    }
    .progress-label {
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #475569;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .progress-bar-track {
        background: #1e293b;
        border-radius: 99px;
        height: 10px;
        overflow: hidden;
        position: relative;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, #00d4ff, #6366f1);
        box-shadow: 0 0 10px rgba(0,212,255,0.5);
        transition: width 0.6s ease;
    }

    /* ── Section Headers ── */
    .section-header {
        font-size: 1rem;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 28px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(0,212,255,0.2), transparent);
    }

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060b18, #080f20) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.1) !important;
    }
    [data-testid="stSidebar"] .stForm {
        background: rgba(13, 21, 38, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-radius: 12px;
        padding: 4px 12px 12px 12px;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 16px 0 2px 0;
    }
    .sidebar-caption {
        font-size: 0.78rem;
        color: #475569;
        margin-bottom: 16px;
    }

    /* ── Report Banner ── */
    .report-banner {
        padding: 22px 26px;
        border-radius: 14px;
        border-left: 5px solid;
        margin-bottom: 24px;
    }
    .report-banner h2 {
        margin: 0 0 8px 0;
        font-size: 1.3rem;
        font-weight: 800;
    }
    .report-banner p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.85;
    }

    /* ── Tab Override ── */
    [data-testid="stTabs"] [role="tab"] {
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.03em;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #00d4ff !important;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #334155;
    }
    .empty-state .icon { font-size: 3.5rem; margin-bottom: 16px; }
    .empty-state h3 { color: #475569; font-weight: 600; margin-bottom: 8px; }
    .empty-state p  { color: #334155; font-size: 0.875rem; }
    </style>
    """, unsafe_allow_html=True)


# ─── State ───────────────────────────────────────────────────────────────────
def initialize_state() -> None:
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "ai_report" not in st.session_state:
        st.session_state.ai_report = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []


# ─── Sidebar ─────────────────────────────────────────────────────────────────
def render_sidebar() -> dict | None:
    st.sidebar.markdown('<div class="sidebar-title">🔐 Hit & Check</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-caption">Cybersecurity awareness simulator for 4-digit demo PINs.</div>', unsafe_allow_html=True)

    with st.sidebar.form("analysis_form"):
        user_name = st.text_input("👤  Name", placeholder="Enter your name")
        email = st.text_input("📧  Email", placeholder="Optional unless sending report")
        pin = st.text_input("🔑  Demo PIN", type="password", max_chars=4, placeholder="4 digits")
        method = st.selectbox("🔒  Transformation", ENCRYPTION_METHODS)
        attack_type = st.selectbox("⚔️  Attack Type", ATTACK_TYPES)
        acknowledged = st.checkbox("I confirm this is not my real ATM or banking PIN.")
        submitted = st.form_submit_button("▶  Run Analysis", use_container_width=True)

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


# ─── Analysis runner ─────────────────────────────────────────────────────────
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


# ─── Dashboard tab ───────────────────────────────────────────────────────────
def render_dashboard() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🛡️</div>
            <h3>No Analysis Yet</h3>
            <p>Enter a demo PIN in the sidebar and click <strong>Run Analysis</strong> to begin.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    attack = analysis["attack_result"]
    score  = analysis["score_result"]
    pin_data = analysis["pin_data"]

    # Metric colour logic
    risk = score["risk_level"].upper()
    score_cls = "green" if score["strength_score_out_of_100"] >= 70 else ("amber" if score["strength_score_out_of_100"] >= 40 else "red")
    prob_cls  = "red"   if score["hack_probability_out_of_100"] >= 70 else ("amber" if score["hack_probability_out_of_100"] >= 30 else "green")
    risk_cls  = "red"   if "HIGH" in risk or "CRITICAL" in risk else ("amber" if "MEDIUM" in risk else "green")

    st.markdown('<div class="section-header">📊 Simulation Results</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Attempts</div>
            <div class="metric-value">{attack['attempts_to_crack']:,}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Strength Score</div>
            <div class="metric-value {score_cls}">{score['strength_score_out_of_100']}<span style="font-size:1rem;color:#475569">/100</span></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Hack Probability</div>
            <div class="metric-value {prob_cls}">{score['hack_probability_out_of_100']}<span style="font-size:1rem;color:#475569">%</span></div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk Level</div>
            <div class="metric-value {risk_cls}" style="font-size:1.4rem">{score['risk_level']}</div>
        </div>""", unsafe_allow_html=True)

    # Info grid
    st.markdown(f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-key">Transformed PIN</div>
            <div class="info-val">{pin_data['encrypted_pin']}</div>
        </div>
        <div class="info-item">
            <div class="info-key">Transformation Method</div>
            <div class="info-val">{pin_data['encryption_method']}</div>
        </div>
        <div class="info-item">
            <div class="info-key">Attack Type</div>
            <div class="info-val">{attack['attack_type']}</div>
        </div>
        <div class="info-item">
            <div class="info-key">Estimated Crack Time</div>
            <div class="info-val">{score['estimated_crack_time_label']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Custom glowing progress bar
    pct = min(attack["crack_position_percentage"] / 100, 1.0)
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">🎯 Crack Position — {attack['crack_position_percentage']:.1f}% through search space</div>
        <div class="progress-bar-track">
            <div class="progress-bar-fill" style="width:{pct*100:.1f}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📈 Search Space Breakdown</div>', unsafe_allow_html=True)
    chart_data = {
        "Metric": ["Attempts Used", "Remaining Search Space"],
        "Count": [
            attack["attempts_to_crack"],
            max(attack["total_possible_combinations"] - attack["attempts_to_crack"], 0),
        ],
    }
    st.bar_chart(chart_data, x="Metric", y="Count")


# ─── AI Report tab ───────────────────────────────────────────────────────────
def render_ai_report() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🤖</div>
            <h3>Run an Analysis First</h3>
            <p>Complete the form in the sidebar to unlock the AI Report.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if st.button("⚡  Generate AI Report", use_container_width=True):
        payload = build_report_payload(analysis)
        st.session_state.ai_report = generate_pin_report(payload)

    report = st.session_state.ai_report
    if not report:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📄</div>
            <h3>Report Not Generated</h3>
            <p>Click the button above to generate detailed AI-powered security guidance.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    risk_level = str(report.get("risk_level", "Unknown")).upper()
    summary = report.get("summary", "No summary available.")

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

    risk_color = "#888888"
    if "HIGH" in risk_level or "CRITICAL" in risk_level:
        risk_color = "#f87171"
    elif "MEDIUM" in risk_level:
        risk_color = "#fbbf24"
    elif "LOW" in risk_level:
        risk_color = "#34d399"

    st.markdown(f"""
    <div class="report-banner" style="background:{risk_color}12; border-color:{risk_color};">
        <h2 style="color:{risk_color};">🛡️ AI Security Report — {risk_level} RISK</h2>
        <p style="color:#cbd5e1;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_strength = go.Figure(go.Indicator(
            mode="gauge+number",
            value=strength_score,
            title={"text": "PIN Strength Score", "font": {"size": 18, "color": "#94a3b8"}},
            gauge={
                "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "#475569"},
                "bar": {"color": "#00d4ff"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 1,
                "bordercolor": "#1e293b",
                "steps": [
                    {"range": [0, 40],  "color": "rgba(248,113,113,0.25)"},
                    {"range": [40, 70], "color": "rgba(251,191,36,0.2)"},
                    {"range": [70, 100],"color": "rgba(52,211,153,0.2)"},
                ],
            }
        ))
        fig_strength.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10),
                                   paper_bgcolor="rgba(0,0,0,0)", font={"color": "#e2e8f0"})
        st.plotly_chart(fig_strength, use_container_width=True)

    with col2:
        fig_hack = go.Figure(go.Indicator(
            mode="gauge+number",
            value=hack_prob,
            title={"text": "Hack Probability (%)", "font": {"size": 18, "color": "#94a3b8"}},
            gauge={
                "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "#475569"},
                "bar": {"color": "#f87171"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 1,
                "bordercolor": "#1e293b",
                "steps": [
                    {"range": [0, 30],  "color": "rgba(52,211,153,0.2)"},
                    {"range": [30, 70], "color": "rgba(251,191,36,0.2)"},
                    {"range": [70, 100],"color": "rgba(248,113,113,0.25)"},
                ],
            }
        ))
        fig_hack.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", font={"color": "#e2e8f0"})
        st.plotly_chart(fig_hack, use_container_width=True)

    st.markdown('<div class="section-header">🔍 Attack Explanation</div>', unsafe_allow_html=True)
    st.info(attack_explanation, icon="💡")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">⚠️ Key Findings</div>', unsafe_allow_html=True)
        if key_findings:
            df_findings = pd.DataFrame({"Findings": key_findings})
            st.dataframe(df_findings, use_container_width=True, hide_index=True)
        else:
            st.info("No key findings reported.")

    with col4:
        st.markdown('<div class="section-header">🛡️ Recommendations</div>', unsafe_allow_html=True)
        if recommendations:
            df_rec = pd.DataFrame({"Actionable Recommendations": recommendations})
            st.dataframe(df_rec, use_container_width=True, hide_index=True)
        else:
            st.info("No recommendations reported.")

    with st.expander("🗂️  Show Raw AI Analysis JSON"):
        st.json(report)


# ─── Chatbot tab ─────────────────────────────────────────────────────────────
def render_chatbot() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">💬</div>
            <h3>Run an Analysis First</h3>
            <p>The assistant needs analysis context before you can chat.</p>
        </div>
        """, unsafe_allow_html=True)
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


# ─── Email tab ───────────────────────────────────────────────────────────────
def render_email_tab() -> None:
    analysis = st.session_state.analysis
    if not analysis:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📧</div>
            <h3>Run an Analysis First</h3>
            <p>Complete an analysis before sending the report via email.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    settings = get_settings()
    current_email = analysis["user"].get("email", "")
    email = st.text_input("📧  Recipient Email", value=current_email)

    if st.button("📤  Send Report via Email", use_container_width=True):
        email_error = validate_email(email, required=True)
        if email_error:
            st.error(email_error)
            return

        report = st.session_state.ai_report or generate_pin_report(build_report_payload(analysis))
        email_report = build_email_report(analysis, report)
        result = send_report_email(email, email_report, settings)
        if result["ok"]:
            st.success("✅  Report email sent successfully.")
        else:
            st.error(result["message"])


# ─── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()
    initialize_state()
    form_data = render_sidebar()
    if form_data:
        run_analysis(form_data)

    # Hero Banner
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">🔐 Cybersecurity Awareness Simulator</div>
        <div class="hero-title">{APP_NAME}</div>
        <p class="hero-subtitle">
            Explore how demo PINs withstand common attack vectors — powered by AI-driven analysis and real security metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Warning banner
    st.markdown("""
    <div class="warning-banner">
        ⚠️&nbsp; <strong>Educational Use Only:</strong>
        Do not enter a real ATM, banking, account, or recovery PIN. Use a demo PIN only.
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📊  Dashboard", "🤖  AI Report", "💬  Security Assistant", "📧  Email Report", "🎓  Awareness Demo"])
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

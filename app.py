"""RealtyFlow — interactive Streamlit frontend.

Run from the repository root:
    streamlit run app.py
"""

from __future__ import annotations

import os
from typing import Any

import streamlit as st
from langchain_core.messages import HumanMessage


st.set_page_config(
    page_title="RealtyFlow · Property Intelligence",
    page_icon="⌂",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink:#1d2b36;
  --navy:#23445b;
  --muted:#6d7d87;
  --paper:#f6f8f5;
  --card:rgba(255,255,255,.86);
  --line:#dce5e5;
  --mint:#dff1e7;
  --green:#3f8f69;
  --coral:#f47d63;
  --gold:#f6c964;
  --blue:#5d94b4;
}

@keyframes pageEnter { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
@keyframes drift { 0%,100% { background-position:88% 3%, 4% 35%; } 50% { background-position:78% 12%, 12% 25%; } }
@keyframes float { 0%,100% { transform:translate3d(0,0,0); } 50% { transform:translate3d(0,-10px,0); } }
@keyframes pulse { 0%,100% { box-shadow:0 0 0 0 rgba(63,143,105,.12), 0 8px 20px rgba(35,68,91,.16); } 50% { box-shadow:0 0 0 9px rgba(63,143,105,0), 0 12px 26px rgba(35,68,91,.2); } }
@keyframes shimmer { from { transform:translateX(-140%) skewX(-18deg); } to { transform:translateX(220%) skewX(-18deg); } }
@keyframes glowDot { 0%,100% { transform:scale(1); opacity:.7; } 50% { transform:scale(1.18); opacity:1; } }

.stApp {
  color:var(--ink);
  font-family:'DM Sans',sans-serif;
  background:
    radial-gradient(circle at 88% 3%, rgba(246,201,100,.21), transparent 22rem),
    radial-gradient(circle at 4% 35%, rgba(223,241,231,.78), transparent 29rem),
    var(--paper);
  animation:drift 18s ease-in-out infinite;
}
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] { background:rgba(255,255,255,.72); border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child { padding-top:2rem; }
section.main > div { position:relative; z-index:1; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; color:var(--ink) !important; letter-spacing:-.04em; }

.brand { display:flex; align-items:center; gap:.65rem; margin-bottom:2.3rem; }
.brand-mark { display:grid; place-items:center; width:2.3rem; height:2.3rem; border-radius:.8rem; background:var(--navy); color:white; font-size:1.28rem; animation:pulse 3.4s ease-in-out infinite; transition:.3s ease; }
.brand:hover .brand-mark { transform:rotate(-8deg) scale(1.08); border-radius:50%; }
.brand-name { font:700 1.12rem 'Space Grotesk'; }
.brand-sub { color:var(--muted); font-size:.69rem; margin-top:-.15rem; }

.hero { padding:2.1rem 0 1.35rem; animation:pageEnter .7s .05s cubic-bezier(.2,.75,.25,1) both; }
.eyebrow { display:inline-flex; align-items:center; gap:.5rem; color:var(--green); font-size:.74rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }
.eyebrow::before { content:""; width:.43rem; height:.43rem; border-radius:50%; background:var(--coral); animation:glowDot 2s ease-in-out infinite; }
.hero h1 { max-width:850px; font-size:clamp(2.8rem,5.7vw,5.5rem); line-height:.96; margin:.7rem 0 1.05rem; background:linear-gradient(110deg,var(--ink) 10%,#3d718d 49%,var(--ink) 85%); background-size:220% auto; -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; animation:headline 7s ease-in-out infinite; }
@keyframes headline { 0%,100% { background-position:0% center; } 50% { background-position:100% center; } }
.hero p { max-width:700px; color:var(--muted); font-size:1.08rem; line-height:1.65; }

.card { position:relative; overflow:hidden; isolation:isolate; background:var(--card); border:1px solid rgba(220,229,229,.9); border-radius:1.3rem; padding:1.35rem 1.45rem; box-shadow:0 12px 38px rgba(35,68,91,.06); animation:pageEnter .7s .14s cubic-bezier(.2,.75,.25,1) both; transition:transform .35s cubic-bezier(.2,.75,.25,1),box-shadow .35s ease,border-color .35s ease; }
.card::after { content:""; position:absolute; inset:0; z-index:-1; width:35%; background:linear-gradient(100deg,transparent,rgba(255,255,255,.62),transparent); transform:translateX(-150%) skewX(-18deg); pointer-events:none; }
.card:hover { transform:translateY(-5px); border-color:rgba(63,143,105,.34); box-shadow:0 20px 52px rgba(35,68,91,.12); }
.card:hover::after { animation:shimmer 1.05s ease-out; }
.kicker { color:var(--muted); font-size:.75rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }
.small-muted { color:var(--muted); font-size:.8rem; line-height:1.5; }

.capability { display:flex; gap:.75rem; align-items:flex-start; padding:.88rem 0; border-bottom:1px solid #edf1f0; transition:.25s ease; }
.capability:last-child { border-bottom:0; }
.capability:hover { padding-left:.5rem; transform:translateX(3px); background:linear-gradient(90deg,rgba(223,241,231,.55),transparent); border-radius:.65rem; }
.cap-icon { width:1.75rem; height:1.75rem; display:grid; place-items:center; flex:0 0 auto; border-radius:.58rem; background:var(--mint); font-size:.9rem; transition:.3s ease; }
.capability:hover .cap-icon { transform:scale(1.12) rotate(5deg); box-shadow:0 6px 15px rgba(63,143,105,.16); }
.cap-title { font-weight:700; font-size:.88rem; }
.cap-copy { color:var(--muted); font-size:.76rem; margin-top:.12rem; }

.example { display:block; padding:.8rem .95rem; margin:.55rem 0; border:1px solid var(--line); border-radius:.75rem; background:rgba(255,255,255,.66); color:var(--navy); font-size:.82rem; transition:.25s ease; }
.example:hover { transform:translateX(4px); border-color:var(--green); background:var(--mint); }

textarea,input { background:#fff !important; border-radius:.78rem !important; transition:border-color .25s ease,box-shadow .25s ease,transform .25s ease !important; }
textarea:focus,input:focus { border-color:var(--green) !important; box-shadow:0 0 0 4px rgba(63,143,105,.12) !important; transform:translateY(-1px); }
div.stButton > button { position:relative; overflow:hidden; isolation:isolate; min-height:2.75rem; border-radius:.78rem; border:1px solid #d1dddd; background:white; color:var(--navy); font-weight:700; transition:transform .25s cubic-bezier(.2,.75,.25,1),box-shadow .25s ease,border-color .25s ease; }
div.stButton > button::after { content:""; position:absolute; inset:0; z-index:-1; width:42%; background:linear-gradient(100deg,transparent,rgba(255,255,255,.45),transparent); transform:translateX(-170%) skewX(-18deg); }
div.stButton > button:hover { transform:translateY(-2px); border-color:var(--green); color:var(--green); box-shadow:0 10px 24px rgba(63,143,105,.13); }
div.stButton > button:hover::after { animation:shimmer .9s ease-out; }
div.stButton > button:active { transform:translateY(1px) scale(.985); }
button[kind="primary"] { background:var(--navy) !important; border-color:var(--navy) !important; color:white !important; box-shadow:0 9px 22px rgba(35,68,91,.17); }
button[kind="primary"]:hover { background:#315d79 !important; color:white !important; box-shadow:0 14px 30px rgba(35,68,91,.24) !important; }

.result-card { background:linear-gradient(145deg,#fff 0%,#f4faf6 100%); border:1px solid #cfe5d8; border-radius:1.2rem; padding:1.35rem 1.5rem; margin-top:.8rem; animation:pageEnter .55s ease both; box-shadow:0 14px 38px rgba(63,143,105,.08); }
.result-head { display:flex; align-items:center; gap:.6rem; color:var(--green); font-size:.75rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }
.result-head::before { content:"✓"; display:grid; place-items:center; width:1.45rem; height:1.45rem; border-radius:50%; color:white; background:var(--green); font-size:.7rem; }
.answer { color:var(--ink); font-size:1.16rem; line-height:1.65; margin-top:.95rem; }
.route-pill { display:inline-flex; align-items:center; gap:.35rem; border:1px solid #cddfe6; border-radius:99px; padding:.35rem .7rem; color:var(--blue); background:#f0f7fa; font-size:.74rem; font-weight:700; }
.property-chip { display:inline-flex; align-items:center; gap:.4rem; border-radius:99px; padding:.4rem .8rem; background:var(--mint); color:#286144; font-size:.78rem; font-weight:700; }
[data-testid="stMetric"] { background:white; border:1px solid var(--line); border-radius:1rem; padding:.8rem 1rem; transition:.3s ease; }
[data-testid="stMetric"]:hover { transform:translateY(-4px); box-shadow:0 14px 30px rgba(35,68,91,.1); border-color:rgba(63,143,105,.34); }
[data-testid="stMetricLabel"] { color:var(--muted); }
[data-testid="stMetricValue"] { color:var(--navy); font-family:'Space Grotesk'; }
hr { border:0; border-top:1px solid var(--line); margin:1.6rem 0; }

@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; scroll-behavior:auto !important; } }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def get_graph():
    from run_command_routing import build_graph
    return build_graph()


def message_content(message: Any) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, list):
        return "\n".join(str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in content)
    return str(content)


def run_realtyflow(query: str) -> dict[str, Any]:
    graph = get_graph()
    return graph.invoke({"messages": [HumanMessage(content=query)]})


def extract_result(final_state: dict[str, Any]) -> tuple[str, str, str]:
    messages = final_state.get("messages", [])
    answer = ""
    route = "Supervisor"
    for message in messages:
        name = getattr(message, "name", None) or ""
        if name and name != "supervisor":
            route = name
        text = message_content(message)
        if name and name != "supervisor" and not text.startswith("Routing to"):
            answer = text
    if not answer and messages:
        answer = message_content(messages[-1])
    return answer, route, final_state.get("property_name", "")


# Sidebar
with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">⌂</div><div><div class="brand-name">RealtyFlow</div><div class="brand-sub">Multi-agent property intelligence</div></div></div>', unsafe_allow_html=True)
    st.markdown("### Agent network")
    st.markdown('<div class="small-muted">Ask a property question and RealtyFlow will route it to the specialist best suited to answer.</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="capability"><div class="cap-icon">⌘</div><div><div class="cap-title">Command supervisor</div><div class="cap-copy">Understands intent and routes dynamically.</div></div></div><div class="capability"><div class="cap-icon">⌂</div><div><div class="cap-title">Property profile</div><div class="cap-copy">Lease terms and property details.</div></div></div><div class="capability"><div class="cap-icon">▦</div><div><div class="cap-title">Transaction history</div><div class="cap-copy">Valuation and price-per-square-foot.</div></div></div><div class="capability"><div class="cap-icon">$</div><div><div class="cap-title">Mortgage affordability</div><div class="cap-copy">Income, rate, and loan calculations.</div></div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Powered by**")
    st.markdown("`LangGraph` · Routing")
    st.markdown("`GPT-4o-mini` · Reasoning")
    st.markdown("`Python tools` · Calculations")
    st.caption("Your question is routed through the existing `run_command_routing.py` graph.")


st.markdown('<div class="hero"><div class="eyebrow">Property intelligence · agentic command routing</div><h1>Ask your property question. Let the right agent do the math.</h1><p>RealtyFlow turns natural-language property questions into focused answers by routing each request through a specialist multi-agent workflow.</p></div>', unsafe_allow_html=True)

left, right = st.columns([1.45, 1], gap="large")
with right:
    st.markdown('<div class="card"><div class="kicker">What you can ask</div><div class="example">⌂ How many years remain on a 99-year lease?</div><div class="example">▦ What is the price per square foot?</div><div class="example">$ How much mortgage can this income support?</div><div class="example">⌘ Tell me about this property profile.</div></div>', unsafe_allow_html=True)

with left:
    st.markdown('<div class="card"><div class="kicker">01 · Start an analysis</div><h2 style="margin:.45rem 0 .35rem;">What would you like to know?</h2><div class="small-muted" style="margin-bottom:.9rem;">Describe the property question naturally. RealtyFlow will identify the intent, extract the property context, and route the request.</div>', unsafe_allow_html=True)
    query = st.text_area("Property question", value=st.session_state.get("query", ""), placeholder="For the property at Sunset Boulevard, which has a 99-year lease starting in January 1995, how many years are remaining on the lease?", height=125, label_visibility="collapsed")
    c1, c2 = st.columns([1.5, 1])
    ask = c1.button("Analyze with RealtyFlow  →", type="primary", use_container_width=True, disabled=not query.strip())
    clear = c2.button("Clear", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if clear:
        st.session_state.pop("query", None)
        st.session_state.pop("result", None)
        st.rerun()

    if ask:
        st.session_state.query = query.strip()
        with st.spinner("Supervisor is routing your question to the right property specialist…"):
            try:
                st.session_state.result = run_realtyflow(query.strip())
            except Exception as exc:
                st.session_state.result_error = str(exc)
        st.rerun()

    if st.session_state.get("result_error"):
        st.error("RealtyFlow could not complete the analysis. Check your environment configuration and try again.")
        with st.expander("Technical details"):
            st.code(st.session_state.result_error)
        st.session_state.pop("result_error", None)

    if st.session_state.get("result"):
        answer, route, property_name = extract_result(st.session_state.result)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="kicker">02 · Intelligence brief</div><h2 style="margin:.45rem 0 .2rem;">Analysis complete</h2>', unsafe_allow_html=True)
        pills = f'<span class="route-pill">↗ Routed to {route.replace("_", " ").title()}</span>'
        if property_name:
            pills += f' <span class="property-chip">⌂ {property_name}</span>'
        st.markdown(pills, unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><div class="result-head">RealtyFlow answer</div><div class="answer">{answer}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("View agent trace"):
            for message in st.session_state.result.get("messages", []):
                name = getattr(message, "name", None) or "user"
                st.markdown(f"**{name.replace('_', ' ').title()}**")
                st.write(message_content(message))

st.markdown("<br>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m1.metric("Routing style", "Command-based")
m2.metric("Specialists", "3 agents")
m3.metric("Frontend", "Interactive")

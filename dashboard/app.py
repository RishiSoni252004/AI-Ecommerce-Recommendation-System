import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import random

# ─── Configuration ───────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL")
if not API_URL:
    st.error("⚠️ API_URL environment variable is not set. Cannot connect to backend.")
    st.stop()

st.set_page_config(
    page_title="ShopSmart — AI-Powered E-Commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Premium CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #0a0a0f;
        --bg-card: #12121a;
        --bg-card-hover: #1a1a28;
        --accent: #6c5ce7;
        --accent-light: #a29bfe;
        --accent-gold: #ffd32a;
        --accent-orange: #ff6b35;
        --text-primary: #ffffff;
        --text-secondary: #8b8b9e;
        --text-muted: #5a5a6e;
        --border: #1e1e2e;
        --success: #00b894;
        --danger: #ff4757;
        --gradient-1: linear-gradient(135deg, #6c5ce7, #a29bfe);
        --gradient-2: linear-gradient(135deg, #ff6b35, #ffd32a);
        --gradient-3: linear-gradient(135deg, #00b894, #55efc4);
    }

    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background: var(--bg-primary) !important;
    }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ─── NAVBAR ───────────────────────────────────── */
    .navbar {
        background: rgba(10, 10, 15, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 20px;
        padding: 1rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .nav-brand {
        font-size: 1.6rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .nav-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .nav-user {
        background: rgba(108, 92, 231, 0.1);
        border: 1px solid rgba(108, 92, 231, 0.25);
        border-radius: 50px;
        padding: 6px 16px 6px 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: white;
    }
    .nav-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--gradient-1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .nav-badge {
        background: var(--accent);
        color: white;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* ─── HERO BANNER ──────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #1a1030 0%, #2d1b69 30%, #6c5ce7 60%, #a29bfe 100%);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 10%;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: rgba(255, 211, 42, 0.08);
    }
    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        color: var(--accent-gold);
        font-size: 0.7rem;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 20px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .hero h1 {
        color: white;
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0 0 0.5rem 0;
        letter-spacing: -1px;
    }
    .hero h1 span {
        background: var(--gradient-2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: rgba(255,255,255,0.65);
        font-size: 1rem;
        margin: 0;
        max-width: 500px;
    }

    /* ─── STATS BAR ────────────────────────────────── */
    .stats-bar {
        display: flex;
        gap: 16px;
        margin-bottom: 2rem;
    }
    .stat-item {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.2rem;
        flex: 1;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-item:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(108, 92, 231, 0.15);
    }
    .stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .stat-label {
        font-size: 0.72rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin: 4px 0 0 0;
    }

    /* ─── SECTION HEADER ───────────────────────────── */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2rem 0 1.2rem 0;
    }
    .sec-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: var(--gradient-1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .sec-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
    }
    .sec-subtitle {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin: 0;
    }

    /* ─── PRODUCT CARD ─────────────────────────────── */
    .p-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 0;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        height: 100%;
    }
    .p-card:hover {
        border-color: var(--accent);
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(108, 92, 231, 0.2);
    }
    .p-card-img {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 2rem;
        text-align: center;
        font-size: 3.5rem;
        position: relative;
    }
    .p-card-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background: var(--danger);
        color: white;
        font-size: 0.6rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 8px;
        letter-spacing: 0.5px;
    }
    .p-card-wishlist {
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .p-card-body {
        padding: 1.2rem;
    }
    .p-card-cat {
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--accent-light);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 6px 0;
    }
    .p-card-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 8px 0;
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .p-card-stars {
        color: var(--accent-gold);
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    .p-card-price-row {
        display: flex;
        align-items: baseline;
        gap: 8px;
    }
    .p-card-price {
        font-size: 1.3rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
    }
    .p-card-mrp {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-decoration: line-through;
        margin: 0;
    }
    .p-card-discount {
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--success);
        margin: 0;
    }

    /* ─── PRODUCT DETAIL ───────────────────────────── */
    .detail-wrap {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .detail-img-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 3rem;
        text-align: center;
        font-size: 6rem;
        border-radius: 20px;
        margin: 1rem;
    }
    .detail-info {
        padding: 1.5rem;
    }
    .detail-name {
        font-size: 1.6rem;
        font-weight: 800;
        color: white;
        margin: 0 0 8px 0;
    }
    .detail-stars {
        color: var(--accent-gold);
        font-size: 0.9rem;
        font-weight: 600;
    }
    .detail-price-box {
        background: rgba(108, 92, 231, 0.08);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    .detail-price {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
    }
    .detail-price small {
        font-size: 1rem;
        color: var(--text-secondary);
    }
    .detail-offer {
        display: inline-block;
        background: rgba(0, 184, 148, 0.15);
        color: var(--success);
        font-size: 0.7rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 8px;
        margin-top: 6px;
    }
    .detail-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    .detail-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .detail-features li {
        color: var(--text-secondary);
        font-size: 0.85rem;
        padding: 6px 0;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .detail-features li::before {
        content: '✓';
        color: var(--success);
        font-weight: 700;
    }

    /* ─── SIDEBAR ──────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #12121a 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--text-secondary) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: var(--accent-light) !important;
        font-weight: 700 !important;
    }

    .sidebar-logo {
        text-align: center;
        padding: 0.5rem 0 1.5rem 0;
    }
    .sidebar-logo-text {
        font-size: 1.5rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .user-card {
        background: rgba(108, 92, 231, 0.06);
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.8rem 0;
        text-align: center;
    }
    .user-avatar-lg {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: var(--gradient-1);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    .user-name-lg {
        font-size: 1rem;
        font-weight: 700;
        color: white !important;
        margin: 0;
    }
    .user-meta-lg {
        font-size: 0.75rem;
        color: var(--text-muted) !important;
        margin: 2px 0 0 0;
    }

    .history-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .h-badge {
        font-size: 0.55rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        flex-shrink: 0;
    }
    .h-view { background: rgba(108,92,231,0.15); color: var(--accent-light) !important; }
    .h-click { background: rgba(255,107,53,0.15); color: var(--accent-orange) !important; }
    .h-purchase { background: rgba(0,184,148,0.15); color: var(--success) !important; }
    .h-text {
        font-size: 0.75rem;
        color: var(--text-secondary) !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .tip-box {
        background: rgba(108, 92, 231, 0.06);
        border: 1px solid rgba(108, 92, 231, 0.12);
        border-radius: 14px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .tip-title {
        font-size: 0.75rem;
        font-weight: 800;
        color: var(--accent-light) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 0 8px 0;
    }
    .tip-step {
        font-size: 0.73rem;
        color: var(--text-muted) !important;
        margin: 3px 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .tip-num {
        background: var(--gradient-1);
        color: white !important;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.6rem;
        font-weight: 700;
        flex-shrink: 0;
    }

    /* ─── BUTTONS ──────────────────────────────────── */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--gradient-1) !important;
        border: none !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(108,92,231,0.1) !important;
        border: 1px solid rgba(108,92,231,0.3) !important;
        color: var(--accent-light) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(108,92,231,0.2) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: 14px;
        padding: 4px;
        gap: 4px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent) !important;
        color: white !important;
    }

    /* ─── FOOTER ───────────────────────────────────── */
    .site-footer {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        margin-top: 3rem;
        text-align: center;
    }
    .footer-brand {
        font-size: 1.3rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .footer-text {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 4px 0;
    }
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin: 1rem 0;
    }
    .footer-link {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 600;
    }
    .footer-tech {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .tech-badge {
        background: rgba(108,92,231,0.08);
        border: 1px solid rgba(108,92,231,0.15);
        color: var(--text-secondary);
        font-size: 0.65rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    /* plotly dark theme */
    .js-plotly-plot .plotly .modebar { display: none !important; }

    /* hide fullscreen buttons on charts */
    button[title="View fullscreen"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─── Data ────────────────────────────────────────────────────────────────────
def fetch_users():
    try:
        res = requests.get(f"{API_URL}/users", timeout=8)
        res.raise_for_status()
        return res.json().get("users", [])
    except Exception as e:
        st.error(f"Failed to fetch users: {e}")
        return []

def fetch_items():
    try:
        res = requests.get(f"{API_URL}/items", timeout=8)
        res.raise_for_status()
        return res.json().get("items", [])
    except Exception as e:
        st.error(f"Failed to fetch items: {e}")
        return []

def fetch_recs(uid):
    try:
        return requests.get(f"{API_URL}/recommendations/{uid}", timeout=5).json().get("recommendations", [])
    except: return []

def fetch_history(uid):
    try:
        return requests.get(f"{API_URL}/users/{uid}/history", timeout=5).json().get("history", [])
    except: return []

def fire_event(uid, iid, action):
    try:
        r = requests.post(f"{API_URL}/event", json={"user_id": uid, "item_id": iid, "action_type": action}, timeout=5)
        if r.status_code == 200:
            icons = {"view": "👁️", "click": "❤️", "purchase": "🛒"}
            st.toast(f"{icons.get(action,'')} {action.capitalize()} recorded!", icon="✅")
            time.sleep(1.5)
            st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")


users = fetch_users()
items = fetch_items()
if not users or not items:
    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem;">
        <p style="font-size:3rem;">🚀</p>
        <p style="color:white; font-size:1.3rem; font-weight:700;">Starting up ShopSmart...</p>
        <p style="color:#8b8b9e; font-size:0.9rem;">Backend services are initializing. Please refresh in a few seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

items_df = pd.DataFrame(items)
items_map = {i["item_id"]: i for i in items}

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-text">🛒 ShopSmart</span>
        <p style="font-size:0.7rem; margin:2px 0 0 0; color:#5a5a6e !important;">AI-Powered E-Commerce</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("##### 👤 Customer Profile")
    umap = {f"{u.get('avatar','👤')} {u['name']}": u for u in users}
    sel_label = st.selectbox("Customer", list(umap.keys()), label_visibility="collapsed")
    sel_user = umap[sel_label]
    uid = sel_user["user_id"]

    st.markdown(f"""
    <div class="user-card">
        <div class="user-avatar-lg">{sel_user.get('avatar','👤')}</div>
        <p class="user-name-lg">{sel_user['name']}</p>
        <p class="user-meta-lg">📍 {sel_user.get('location','')} · 🎂 Age {sel_user.get('age','?')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("##### 🕐 Browsing History")
    hist = fetch_history(uid)
    if hist:
        for h in hist[:6]:
            iname = items_map.get(h.get("item_id"),{}).get("title","Item")
            act = h.get("action_type","view")
            css = f"h-{act}"
            st.markdown(f"""
            <div class="history-card">
                <span class="h-badge {css}">{act}</span>
                <span class="h-text">{iname}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No activity yet — start shopping!")

    st.markdown("---")

    st.markdown("""
    <div class="tip-box">
        <p class="tip-title">🧠 How AI Recs Work</p>
        <p class="tip-step"><span class="tip-num">1</span> Browse & interact with products</p>
        <p class="tip-step"><span class="tip-num">2</span> Events stream through Kafka in real-time</p>
        <p class="tip-step"><span class="tip-num">3</span> ML model computes cosine similarity</p>
        <p class="tip-step"><span class="tip-num">4</span> Top 5 picks cached in Redis instantly</p>
    </div>
    """, unsafe_allow_html=True)


# ─── Navbar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <span class="nav-brand">🛒 ShopSmart</span>
    <div class="nav-right">
        <span class="nav-badge">⚡ AI Powered</span>
        <div class="nav-user">
            <div class="nav-avatar">{sel_user.get('avatar','👤')}</div>
            <span style="font-size:0.85rem; font-weight:600;">{sel_user['name']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <span class="hero-tag">✨ Personalized for you</span>
    <h1>Discover Products You'll <span>Love</span></h1>
    <p>Our AI analyzes your behavior in real-time to recommend exactly what you're looking for. The more you browse, the smarter it gets.</p>
</div>
""", unsafe_allow_html=True)


# ─── Stats Bar ───────────────────────────────────────────────────────────────
n_cats = items_df["category"].nunique() if not items_df.empty else 0
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <p class="stat-num">{len(users)}</p>
        <p class="stat-label">Customers</p>
    </div>
    <div class="stat-item">
        <p class="stat-num">{len(items)}</p>
        <p class="stat-label">Products</p>
    </div>
    <div class="stat-item">
        <p class="stat-num">{n_cats}</p>
        <p class="stat-label">Categories</p>
    </div>
    <div class="stat-item">
        <p class="stat-num" style="-webkit-text-fill-color:#00b894;">Live</p>
        <p class="stat-label">AI Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Helper: render product card ─────────────────────────────────────────────
def render_card(item, key_prefix):
    price = item.get("price", 0)
    mrp = int(price * random.uniform(1.15, 1.45))
    discount = int((1 - price / mrp) * 100)
    rating = item.get("rating", 0)
    stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))

    st.markdown(f"""
    <div class="p-card">
        <div class="p-card-img">
            <span class="p-card-badge">{discount}% OFF</span>
            <span class="p-card-wishlist">♡</span>
            {item.get('image','📦')}
        </div>
        <div class="p-card-body">
            <p class="p-card-cat">{item.get('category','')}</p>
            <p class="p-card-name">{item.get('title','')}</p>
            <p class="p-card-stars">{stars} {rating}</p>
            <div class="p-card-price-row">
                <p class="p-card-price">₹{price:,}</p>
                <p class="p-card-mrp">₹{mrp:,}</p>
                <p class="p-card-discount">{discount}% off</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("👁️ View", key=f"{key_prefix}_v", use_container_width=True):
            st.session_state.selected_product = item["item_id"]
            fire_event(uid, item["item_id"], "view")
    with c2:
        if st.button("🛒 Buy", key=f"{key_prefix}_b", use_container_width=True, type="primary"):
            fire_event(uid, item["item_id"], "purchase")


# ─── Recommended For You ─────────────────────────────────────────────────────
recs = fetch_recs(uid)

st.markdown(f"""
<div class="sec-header">
    <div class="sec-icon">⚡</div>
    <div>
        <p class="sec-title">Recommended for {sel_user['name'].split()[0]}</p>
        <p class="sec-subtitle">Curated by our AI based on your activity</p>
    </div>
</div>
""", unsafe_allow_html=True)

if recs:
    cols = st.columns(5)
    for i, rec in enumerate(recs[:5]):
        with cols[i]:
            render_card(rec, f"rec_{i}")
else:
    st.markdown("""
    <div style="background:rgba(108,92,231,0.06); border:1px solid rgba(108,92,231,0.15); border-radius:16px; padding:2rem; text-align:center; margin:1rem 0;">
        <p style="font-size:2rem; margin:0;">🛍️</p>
        <p style="color:white; font-weight:700; margin:8px 0 4px 0;">Start Shopping!</p>
        <p style="color:#8b8b9e; font-size:0.85rem; margin:0;">Browse products below and interact to get personalized AI recommendations</p>
    </div>
    """, unsafe_allow_html=True)


# ─── Product Detail ──────────────────────────────────────────────────────────
if st.session_state.selected_product and st.session_state.selected_product in items_map:
    prod = items_map[st.session_state.selected_product]
    price = prod.get("price", 0)
    mrp = int(price * 1.3)
    discount = int((1 - price / mrp) * 100)
    rating = prod.get("rating", 0)
    stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))

    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-icon">🔍</div>
        <div>
            <p class="sec-title">Product Details</p>
            <p class="sec-subtitle">Everything you need to know</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    d1, d2 = st.columns([2, 3])
    with d1:
        st.markdown(f"""
        <div class="detail-img-box">{prod.get('image','📦')}</div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="detail-info">
            <p style="font-size:0.7rem; font-weight:700; color:#a29bfe; text-transform:uppercase; letter-spacing:1.5px; margin:0 0 8px 0;">{prod.get('category','')}</p>
            <p class="detail-name">{prod.get('title','')}</p>
            <p class="detail-stars">{stars} {rating}/5.0 · Community Favorite</p>
            <div class="detail-price-box">
                <p class="detail-price">₹{price:,} <small><s>₹{mrp:,}</s></small></p>
                <span class="detail-offer">🎉 Save ₹{mrp - price:,} ({discount}% off)</span>
            </div>
            <p class="detail-desc">{prod.get('description','')}</p>
            <ul class="detail-features">
                <li>Free Delivery by Tomorrow</li>
                <li>7-Day Easy Returns</li>
                <li>Top Rated by Community</li>
                <li>Secure Payment Options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🛒 Add to Cart", key="det_buy", type="primary", use_container_width=True):
                fire_event(uid, prod["item_id"], "purchase")
        with b2:
            if st.button("❤️ Wishlist", key="det_wish", type="secondary", use_container_width=True):
                fire_event(uid, prod["item_id"], "click")
        with b3:
            if st.button("🔗 Share", key="det_share", type="secondary", use_container_width=True):
                fire_event(uid, prod["item_id"], "view")

    # Similar products
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-icon">🔄</div>
        <div>
            <p class="sec-title">Customers Also Viewed</p>
            <p class="sec-subtitle">Similar products you might like</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    same_cat = [it for it in items if it.get("category") == prod.get("category") and it["item_id"] != prod["item_id"]]
    if len(same_cat) < 5:
        others = [it for it in items if it["item_id"] != prod["item_id"] and it not in same_cat]
        others.sort(key=lambda x: x.get("rating",0), reverse=True)
        same_cat.extend(others[:5-len(same_cat)])

    scols = st.columns(min(len(same_cat), 5))
    for i, s in enumerate(same_cat[:5]):
        with scols[i]:
            render_card(s, f"sim_{i}")


# ─── Shop by Category ────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <div class="sec-icon">📁</div>
    <div>
        <p class="sec-title">Shop by Category</p>
        <p class="sec-subtitle">Browse our complete catalog</p>
    </div>
</div>
""", unsafe_allow_html=True)

cats = sorted(items_df["category"].unique().tolist())
cat_tabs = st.tabs(cats)

for idx, cat in enumerate(cats):
    with cat_tabs[idx]:
        citems = [it for it in items if it.get("category") == cat]
        n = min(len(citems), 5)
        cols = st.columns(n)
        for j, item in enumerate(citems[:n]):
            with cols[j]:
                render_card(item, f"cat_{cat}_{j}")


# ─── Analytics ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <div class="sec-icon">📊</div>
    <div>
        <p class="sec-title">Platform Analytics</p>
        <p class="sec-subtitle">Real-time insights from our recommendation engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

a1, a2 = st.columns(2)
with a1:
    top = items_df.nlargest(10, "rating")
    fig = px.bar(top, x="title", y="rating", color="category",
                 color_discrete_sequence=["#6c5ce7","#a29bfe","#ff6b35","#ffd32a","#00b894","#ff4757"],
                 title="🏆 Top 10 Highest-Rated Products")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", size=11, color="#8b8b9e"),
        title_font=dict(size=14, color="white"),
        xaxis=dict(tickangle=-45, gridcolor="rgba(30,30,46,0.5)"),
        yaxis=dict(gridcolor="rgba(30,30,46,0.5)"),
        margin=dict(t=50, b=120), legend=dict(font=dict(color="#8b8b9e")),
    )
    st.plotly_chart(fig, use_container_width=True)

with a2:
    cc = items_df["category"].value_counts().reset_index()
    cc.columns = ["Category", "Products"]
    fig2 = px.pie(cc, names="Category", values="Products",
                  color_discrete_sequence=["#6c5ce7","#a29bfe","#ff6b35","#ffd32a","#00b894","#ff4757"],
                  title="📁 Product Distribution", hole=0.5)
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", size=11, color="#8b8b9e"),
        title_font=dict(size=14, color="white"),
        legend=dict(font=dict(color="#8b8b9e")),
    )
    st.plotly_chart(fig2, use_container_width=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">🛒 ShopSmart</div>
    <p class="footer-text">Real-Time AI-Powered Recommendation System</p>
    <div class="footer-links">
        <span class="footer-link">About</span>
        <span class="footer-link">Privacy</span>
        <span class="footer-link">Terms</span>
        <span class="footer-link">Contact</span>
        <span class="footer-link">Careers</span>
    </div>
    <div class="footer-tech">
        <span class="tech-badge">FastAPI</span>
        <span class="tech-badge">Apache Kafka</span>
        <span class="tech-badge">Scikit-learn</span>
        <span class="tech-badge">MongoDB</span>
        <span class="tech-badge">Redis</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Docker</span>
    </div>
    <p class="footer-text" style="margin-top:1rem; opacity:0.4;">© 2026 ShopSmart · Cloud Engineering Project</p>
</div>
""", unsafe_allow_html=True)

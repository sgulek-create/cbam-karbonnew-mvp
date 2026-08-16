import streamlit as st

st.set_page_config(
    page_title="AB CBAM Karbon Muhasebesi MVP",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ELECTRICITY_FACTOR_KG = 0.450  # kg CO2e / kWh (Scope 2, şebeke varsayılanı)
NATURAL_GAS_FACTOR_KG = 2.020  # kg CO2e / Sm³ (Scope 1, yanma varsayılanı)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #0b1f33 0%, #10263d 42%, #0e1a28 100%);
        color: #e8eef4;
    }
    [data-testid="stNumberInput"] input,
    input[type="number"],
    input[type="text"] {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        background-color: #ffffff !important;
        caret-color: #111111 !important;
        min-height: 44px !important;
        font-size: 16px !important;
    }
    h1, h2, h3 {
        color: #f4f8fb !important;
        letter-spacing: 0.02em;
        overflow-wrap: anywhere;
        word-break: break-word;
    }
    .hero-kicker {
        color: #7eb6d9;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .hero-sub {
        color: #b7c7d6;
        font-size: 1.02rem;
        margin-bottom: 1.4rem;
    }
    div[data-testid="stMetric"] {
        background: #13283d;
        border: 1px solid #2a4d6e;
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
    }
    div[data-testid="stMetric"] label {
        color: #9db6c9 !important;
        white-space: normal !important;
    }
    div[data-testid="stMetricValue"] {
        color: #f7fbff !important;
        overflow-wrap: anywhere;
    }
    .stButton > button {
        background: #1c6ea4;
        color: #fff;
        border: 0;
        border-radius: 8px;
        font-weight: 600;
        min-height: 44px;
    }
    .footnote {
        color: #8ea3b5;
        font-size: 0.85rem;
        line-height: 1.45;
        margin-top: 1.2rem;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
    }
    .stApp > header {
        background: transparent;
    }
    @media (max-width: 900px) {
        .stApp { font-size: 15px; }
        .block-container {
            padding: 0.7rem 0.75rem 2.2rem !important;
            max-width: 100% !important;
        }
        h1 { font-size: 1.35rem !important; line-height: 1.25 !important; }
        h2, h3 { font-size: 1.05rem !important; }
        .hero-kicker { font-size: 0.66rem; letter-spacing: 0.1em; }
        .hero-sub { font-size: 0.9rem; margin-bottom: 0.8rem; }
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.55rem !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        div[data-testid="stMetric"] { padding: 12px; }
        div[data-testid="stMetricValue"] { font-size: 1.25rem !important; }
        .stButton > button { width: 100%; }
        .footnote { font-size: 0.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def calculate_emissions(
    electricity_kwh: float,
    natural_gas_sm3: float,
    electricity_factor: float,
    natural_gas_factor: float,
) -> dict[str, float]:
    scope_2 = (electricity_kwh * electricity_factor) / 1000
    scope_1 = (natural_gas_sm3 * natural_gas_factor) / 1000
    return {
        "scope_1": scope_1,
        "scope_2": scope_2,
        "total": scope_1 + scope_2,
    }


st.markdown('<div class="hero-kicker">AB CBAM · Karbon muhasebesi MVP</div>', unsafe_allow_html=True)
st.title("Sanayi tesisi karbon ayak izi")
st.markdown(
    '<p class="hero-sub">İhracatçılar ve üretim tesisleri için Scope 1, Scope 2 ve toplam emisyonun '
    "tCO2e cinsinden anlık hesabı.</p>",
    unsafe_allow_html=True,
)

with st.expander("Tesis girdileri", expanded=True):
    electricity_kwh = st.number_input(
        "Elektrik tüketimi (kWh)",
        min_value=0.0,
        value=50_000.0,
        step=1.0,
        format="%.2f",
    )
    natural_gas_sm3 = st.number_input(
        "Doğalgaz tüketimi (Sm³)",
        min_value=0.0,
        value=8_000.0,
        step=1.0,
        format="%.2f",
    )
    st.caption("Sayıyı yazıp Enter’a basın.")

    with st.expander("Emisyon faktörleri (gelişmiş)"):
        electricity_factor = st.number_input(
            "Elektrik (kg CO2e / kWh)",
            min_value=0.0,
            value=ELECTRICITY_FACTOR_KG,
            step=0.001,
            format="%.3f",
        )
        natural_gas_factor = st.number_input(
            "Doğalgaz (kg CO2e / Sm³)",
            min_value=0.0,
            value=NATURAL_GAS_FACTOR_KG,
            step=0.001,
            format="%.3f",
        )
        st.caption("Varsayılanlar MVP içindir. Resmi CBAM beyanında ülke/tesis özel faktör gerekir.")

results = calculate_emissions(
    electricity_kwh,
    natural_gas_sm3,
    electricity_factor,
    natural_gas_factor,
)

col1, col2, col3 = st.columns(3)
col1.metric("Scope 1 (Doğalgaz)", f"{results['scope_1']:,.2f} tCO2e")
col2.metric("Scope 2 (Elektrik)", f"{results['scope_2']:,.2f} tCO2e")
col3.metric("Toplam karbon ayak izi", f"{results['total']:,.2f} tCO2e")

st.subheader("Emisyon dağılımı")
st.bar_chart(
    {
        "tCO2e": {
            "Scope 1": results["scope_1"],
            "Scope 2": results["scope_2"],
        }
    },
    color="#3d9ad1",
    height=240,
)

left, right = st.columns(2)
with left:
    st.markdown("**Hesaplama**")
    st.code(
        f"Scope 1 = doğalgaz (Sm³) × {natural_gas_factor:.3f} / 1000\n"
        f"Scope 2 = elektrik (kWh) × {electricity_factor:.3f} / 1000\n"
        "Toplam  = Scope 1 + Scope 2   → tCO2e",
        language="text",
    )
with right:
    st.markdown("**Bu dönem girdileri**")
    st.write(f"- Elektrik: **{electricity_kwh:,.1f} kWh**")
    st.write(f"- Doğalgaz: **{natural_gas_sm3:,.1f} Sm³**")

st.markdown(
    '<p class="footnote">Bu araç ön muhasebe ve farkındalık içindir. AB CBAM bildirimi; doğrulanmış '
    "emisyon faktörleri, ürün bazlı gömülü emisyon, varsayılan değerler ve yetkili doğrulayıcı süreci gerektirir. "
    "Buradaki sonuçlar yasal beyan yerine geçmez.</p>",
    unsafe_allow_html=True,
)

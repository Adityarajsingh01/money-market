# app.py

```python
# ============================================================
# SR1-ZQ INSTITUTIONAL LIQUIDITY DASHBOARD
# Streamlit App
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="SR1-ZQ Institutional Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f14;
        color: #d7dde8;
    }

    .metric-card {
        background-color: #11161f;
        border: 1px solid rgba(255,255,255,0.06);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
    }

    .panel-card {
        background-color: #11161f;
        border: 1px solid rgba(255,255,255,0.06);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 14px;
    }

    .big-number {
        font-size: 34px;
        font-weight: 700;
    }

    .panel-title {
        font-size: 20px;
        font-weight: 600;
        color: #7dd3fc;
        margin-bottom: 18px;
    }

    .small-label {
        color: #94a3b8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("SR1-ZQ Dashboard")

view_mode = st.sidebar.selectbox(
    "Dashboard Mode",
    [
        "Live Market",
        "Stress Scenario",
        "Liquidity Crisis",
        "Fed Easing Cycle",
    ],
)

contract_focus = st.sidebar.selectbox(
    "Curve Focus",
    ["SR1", "SR3", "ZQ", "Whites", "Reds", "Greens", "Blues"],
)

st.sidebar.markdown("---")
show_stress = st.sidebar.checkbox("Show Crisis Metrics", True)
show_cross = st.sidebar.checkbox("Show Cross Asset", True)
show_positioning = st.sidebar.checkbox("Show Positioning", True)

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(
        """
        <div style='padding-top:10px;'>
            <div style='font-size:34px;font-weight:700;color:#60a5fa;'>
                SR1-ZQ Institutional Liquidity Dashboard
            </div>
            <div style='color:#94a3b8;font-size:14px;'>
                Macro Liquidity • Repo Stress • Fed Path • STIR Relative Value
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.metric("Liquidity Regime", "71", "+4")

metrics = [
    ("SOFR", "4.33%", "+0bp"),
    ("EFFR", "4.33%", "0bp"),
    ("SOFR-IORB", "-7bp", "Neutral"),
    ("ON RRP", "$87bn", "-14bn"),
    ("TGA", "$820bn", "+22bn"),
    ("Reserves", "$3.26tn", "-12bn"),
    ("FRA-OIS", "31bp", "+2bp"),
    ("MOVE", "112", "+5"),
]

cols = st.columns(8)

for col, metric in zip(cols, metrics):
    with col:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-label'>{metric[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-number'>{metric[1]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#94a3b8;font-size:13px'>{metric[2]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1.1, 1.2, 0.9])

with left:

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Fed Path Engine</div>", unsafe_allow_html=True)

    meetings = pd.DataFrame(
        {
            "Meeting": ["Apr", "Jun", "Jul", "Sep", "Oct", "Dec"],
            "Implied Rate": [4.37, 4.12, 3.87, 3.62, 3.50, 3.37],
            "Cut Probability": [8, 72, 84, 92, 95, 97],
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=meetings["Meeting"],
            y=meetings["Implied Rate"],
            mode="lines+markers",
            name="Fed Path",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#11161f",
        plot_bgcolor="#11161f",
        height=300,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(meetings, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Liquidity Regime Engine</div>", unsafe_allow_html=True)

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=71,
            title={"text": "Liquidity Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#10b981"},
            },
        )
    )

    gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="#11161f",
        height=300,
    )

    st.plotly_chart(gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with center:

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Relative Value Engine</div>", unsafe_allow_html=True)

    rv_df = pd.DataFrame(
        {
            "Metric": ["SOFR-EFFR", "FRA-OIS", "SR1-SR3", "Bill-OIS", "GC-EFFR"],
            "Value": [0.0, 31, -1.5, 7, 3],
            "Percentile": [48, 82, 63, 71, 66],
            "Signal": ["Neutral", "Stress", "Watch", "Tight", "Pressure"],
        }
    )

    st.dataframe(rv_df, use_container_width=True)

    heatmap = np.random.randn(6, 6)

    fig2 = px.imshow(
        heatmap,
        color_continuous_scale="RdYlGn",
        aspect="auto",
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#11161f",
        plot_bgcolor="#11161f",
        height=350,
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Seasonality Engine</div>", unsafe_allow_html=True)

    seasonality_df = pd.DataFrame(
        {
            "Month": ["Apr", "Jun", "Sep", "Dec", "Jan"],
            "Stress": [82, 91, 95, 99, 30],
        }
    )

    fig3 = px.bar(seasonality_df, x="Month", y="Stress", color="Stress")

    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#11161f",
        plot_bgcolor="#11161f",
        height=320,
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:

    if show_stress:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>Stress & Crisis Monitor</div>", unsafe_allow_html=True)

        stress_df = pd.DataFrame(
            {
                "Metric": ["Repo Fails", "Cross Currency Basis", "SRF Usage", "CDX Financials", "MOVE"],
                "Value": [412, -41, 4, 121, 112],
            }
        )

        st.dataframe(stress_df, use_container_width=True)
        st.warning("Current regime resembles Sep 2019 Repo Stress")
        st.markdown("</div>", unsafe_allow_html=True)

    if show_cross:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>Cross Asset Confirmation</div>", unsafe_allow_html=True)

        cross_df = pd.DataFrame(
            {
                "Asset": ["2Y Yield", "DXY", "USDJPY", "HY Spreads", "Regional Banks", "Oil"],
                "Signal": [
                    "Cuts Confirmed",
                    "USD Softening",
                    "Divergence",
                    "Risk Off",
                    "Funding Stress",
                    "Disinflationary",
                ],
            }
        )

        st.dataframe(cross_df, use_container_width=True)
        st.success("Cross asset confirms liquidity-driven bull steepening")
        st.markdown("</div>", unsafe_allow_html=True)

    if show_positioning:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>Positioning Engine</div>", unsafe_allow_html=True)

        positioning = pd.DataFrame(
            {
                "Category": ["Leveraged Funds", "Dealer Gamma", "Roll Pressure"],
                "Score": [88, 62, 71],
            }
        )

        fig4 = px.bar(positioning, x="Category", y="Score", color="Score")

        fig4.update_layout(
            template="plotly_dark",
            paper_bgcolor="#11161f",
            plot_bgcolor="#11161f",
            height=300,
        )

        st.plotly_chart(fig4, use_container_width=True)
        st.info("Leveraged funds heavily long deferred cuts")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
# ============================================================
# EXTRA INSTITUTIONAL PANELS
# ============================================================

st.markdown('---')

extra1, extra2, extra3 = st.columns(3)

with extra1:
    st.subheader('Funding Stress Dashboard')

    funding_df = pd.DataFrame({
        'Metric': [
            'SOFR-EFFR',
            'Triparty Repo',
            'GC Repo',
            'Fails To Deliver',
            'Dealer Balance Sheet',
            'Fed SRF Usage'
        ],
        'Current': [
            '-7bp',
            '4.39%',
            '4.36%',
            '412bn',
            'Tight',
            '4bn'
        ],
        'Signal': [
            'Ample',
            'Stable',
            'Neutral',
            'Stress',
            'Constraint',
            'Low Usage'
        ]
    })

    st.dataframe(funding_df, use_container_width=True)

with extra2:
    st.subheader('Curve RV Monitor')

    curve_df = pd.DataFrame({
        'Structure': [
            'Whites Reds',
            'Reds Greens',
            'Greens Blues',
            'EDM Fly',
            'ZQ/SR1 Basis',
            '1Y1Y OIS'
        ],
        'ZScore': [-1.8, 0.6, 1.4, -2.2, 1.1, -0.9],
        'Signal': [
            'Rich',
            'Neutral',
            'Cheap',
            'Dislocated',
            'Wide',
            'Neutral'
        ]
    })

    st.dataframe(curve_df, use_container_width=True)

with extra3:
    st.subheader('Macro Liquidity Drivers')

    liquidity_macro = pd.DataFrame({
        'Driver': [
            'QT Pace',
            'Treasury Issuance',
            'Coupon Settlement',
            'Bank Reserves',
            'RRP Drawdown',
            'Foreign Demand'
        ],
        'Impact': [
            'Bearish Liquidity',
            'Drain',
            'Temporary Tightening',
            'Supportive',
            'Bullish',
            'USD Funding Tight'
        ]
    })

    st.dataframe(liquidity_macro, use_container_width=True)

st.markdown('---')

signal1, signal2 = st.columns([1.3, 1])

with signal1:
    st.subheader('Institutional Trade Signals')

    trade_df = pd.DataFrame({
        'Trade': [
            'Receive Reds',
            'Receive Greens',
            'Whites/Greens Steepener',
            'Long Dec SR1',
            'Long ZQ/SR1 Basis'
        ],
        'Conviction': [88, 79, 83, 74, 69],
        'Theme': [
            'Fed Cuts',
            'Growth Slowdown',
            'Bull Steepener',
            'Front-End Rally',
            'Funding Stress'
        ]
    })

    st.dataframe(trade_df, use_container_width=True)

with signal2:
    st.subheader('Event Risk Matrix')

    risk_df = pd.DataFrame({
        'Event': [
            'CPI',
            'Payrolls',
            'Refunding',
            'FOMC',
            'Quarter-End',
            'Debt Ceiling'
        ],
        'Risk': [92, 81, 74, 99, 89, 62]
    })

    fig_risk = px.bar(risk_df, x='Event', y='Risk', color='Risk')

    fig_risk.update_layout(
        template='plotly_dark',
        paper_bgcolor='#11161f',
        plot_bgcolor='#11161f',
        height=350,
    )

    st.plotly_chart(fig_risk, use_container_width=True)

st.caption(f"Institutional SR1-ZQ Dashboard • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

---

# requirements.txt

```txt
streamlit
pandas
numpy
plotly
```

---

# GITHUB + STREAMLIT DEPLOYMENT

## 1. Create GitHub Repository

Repository name example:

```txt
sr1-zq-dashboard
```

---

## 2. Upload Files

Upload:

* app.py
* requirements.txt

---

## 3. Deploy On Streamlit

Go to:

```txt
https://streamlit.io/cloud
```

Then:

* Sign in with GitHub
* New App
* Select repository
* Main file path:

```txt
app.py
```

* Click Deploy

---

# LOCAL RUN

```bash
pip install -r requirements.txt
streamlit run app.py
```

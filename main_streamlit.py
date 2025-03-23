import streamlit as st
import pandas as pd
from main import EnhancedStockAnalyzer
import plotly.graph_objects as go
import torch

st.set_page_config(
    page_title="Stock Market Agent",
    page_icon="📈",
    layout="wide"
)
st.title("📈 Stock Market Agent")

@st.cache_resource
def load_analyzer():
    return EnhancedStockAnalyzer()
try:
    analyzer = load_analyzer()
    analyzer.load_stock_data("stock_data.csv")
    st.success("✅ Model and data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model or data: {str(e)}")
    st.stop()

st.sidebar.header("Stock Filters")

industries = analyzer.stock_data['industry'].dropna().unique().tolist() if 'industry' in analyzer.stock_data.columns else []
industry_list = ['All'] + sorted(industries)

selected_industry = st.sidebar.selectbox(
    "Filter by Industry",
    options=industry_list
)

if selected_industry == "All":
    filtered_stocks = analyzer.stock_data
else:
    filtered_stocks = analyzer.stock_data[analyzer.stock_data['industry'] == selected_industry]

stock_options = filtered_stocks['symbol'].tolist()

def format_stock_display(symbol):
    # handling NIFTY 50 separately
    if symbol == "NIFTY 50":
        return "NIFTY 50"

    stock_data = analyzer.stock_data[analyzer.stock_data['symbol'] == symbol]
    if stock_data.empty:
        return symbol

    company_name = stock_data['companyName'].iloc[0]
    if pd.notna(company_name):
        return f"{symbol} - {company_name}"

    return symbol

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    options=stock_options,
    format_func=format_stock_display
)

if st.button("Analyze Stock"):
    with st.spinner("Analyzing stock..."):
        analysis = analyzer.analyze_stock(selected_stock)

        if "error" in analysis:
            st.error(f"Error in analysis: {analysis['error']}")
        else:
            st.subheader("📊 Market Overview")
            company_name = analysis['basic_info']['company']
            symbol = analysis['basic_info']['symbol']
            industry = analysis['basic_info']['industry']

            if symbol == "NIFTY 50":
                company_name = "NSE Indices"
                industry = "Market Index"

            st.write(f"""
            **{company_name}** ({symbol}) | {industry}
            Current Price: ₹{analysis['price_data']['current_price']:,.2f} ({analysis['performance']['daily_change']:+.2f}%)
            """)

            st.subheader("🤖 AI Summary")

            st.markdown("#### 📈 Key Stock Insights")
            st.write(f"Analysis as of {pd.Timestamp.now().strftime('%Y-%m-%d')}")

            summary_tab, metrics_tab, details_tab = st.tabs(["Analysis Summary", "Key Metrics", "Detailed Insights"])

            with summary_tab:
                daily_change = analysis['performance']['daily_change']
                daily_change_color = "red" if daily_change < 0 else "green"
                daily_change_arrow = "↓" if daily_change < 0 else "↑"

                st.metric(
                    "Current Trading Price",
                    f"₹{analysis['price_data']['current_price']:,.2f}",
                    f"{daily_change_arrow} {daily_change:+.2f}% Today",
                    delta_color="normal"  
                )

            with metrics_tab:
                col1, col2, col3 = st.columns(3)

                def format_delta(value, prefix=""):
                    arrow = "↓" if value < 0 else "↑"
                    return f"{prefix}{arrow} {value:+.2f}%"

                with col1:
                    year_low = analysis['price_data']['year_range']['low']
                    st.metric(
                        "Price Range",
                        f"₹{analysis['price_data']['year_range']['high']:,.2f}",
                        format_delta(year_low, "Low: ₹"),
                        delta_color="normal"
                    )

                with col2:
                    yearly_change = analysis['performance']['yearly_change']
                    monthly_change = analysis['performance']['monthly_change']
                    st.metric(
                        "Performance",
                        format_delta(yearly_change) + " (1Y)",
                        format_delta(monthly_change) + " (1M)",
                        delta_color="normal"
                    )

                with col3:
                    daily_change = analysis['performance']['daily_change']
                    st.metric(
                        "Trading Activity",
                        f"₹{analysis['trading_info']['value_cr']:,.0f}Cr",
                        format_delta(daily_change),
                        delta_color="normal"
                    )

            with details_tab:
                for category, (icon, color) in [
                    ('growth', ('📈', 'green')),
                    ('valuation', ('⚖️', 'orange')),
                    ('technical', ('📊', 'blue')),
                    ('market', ('🌍', 'red')),
                    ('strategy', ('💡', 'purple'))
                ]:
                    if analysis['insights'][category]['details']:
                        with st.expander(f"{icon} {analysis['insights'][category]['title']}"):
                            for detail in analysis['insights'][category]['details']:
                                st.markdown(f"• {detail}")

            st.subheader("📈 Performance Metrics")
            col1, col2, col3 = st.columns(3)

            with col1:
                yearly_change = analysis['performance']['yearly_change']
                st.metric(
                    "1 Year Change",
                    f"{yearly_change:+.2f}%",
                    f"High: ₹{analysis['price_data']['year_range']['high']:,.2f}",
                    delta_color="normal"
                )

            with col2:
                monthly_change = analysis['performance']['monthly_change']
                st.metric(
                    "30 Day Change",
                    f"{monthly_change:+.2f}%",
                    f"Low: ₹{analysis['price_data']['year_range']['low']:,.2f}",
                    delta_color="normal"
                )

            with col3:
                daily_change = analysis['performance']['daily_change']
                st.metric(
                    "Trading Value",
                    f"₹{analysis['trading_info']['value_cr']:,.0f}Cr",
                    format_delta(daily_change),
                    delta_color="normal"
                )

            performance_data = {
                'periods': ['Daily', '30 Days', '1 Year'],
                'changes': [
                    analysis['performance']['daily_change'],
                    analysis['performance']['monthly_change'],
                    analysis['performance']['yearly_change']
                ]
            }

            colors = ['#00ff00' if change >= 0 else '#ff0000'
                     for change in performance_data['changes']]

            fig = go.Figure(data=[
                go.Bar(
                    x=performance_data['periods'],
                    y=performance_data['changes'],
                    marker_color=colors
                )
            ])

            fig.update_layout(
                title="Performance Comparison",
                yaxis_title="Change %",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
                xaxis=dict(gridcolor='rgba(128,128,128,0.1)')
            )

            st.plotly_chart(fig, use_container_width=True)
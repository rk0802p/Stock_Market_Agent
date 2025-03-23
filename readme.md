# Stock Market Analysis Tool

A comprehensive stock market analysis tool that combines traditional technical analysis with AI-powered insights. The tool features a Streamlit web interface for interactive visualization and analysis.

## Features

- Real-time stock data scraping from NSE India
- AI-powered stock analysis using T5 transformer model
- Interactive web interface with Streamlit
- Comprehensive technical analysis including:
  - Growth metrics
  - Valuation risks
  - Technical signals
  - Market risks
  - Investment strategies
- Interactive visualizations with Plotly
- Industry-based filtering
- Detailed performance metrics and insights

## Project Structure

- `main.py`: Core analysis engine with AI integration
- `main_streamlit.py`: Web interface implementation
- `scrapper.py`: NSE India data scraper
- `data_formatting.py`: Data processing and formatting utilities
- `stock_data.csv`: Processed stock data
- `stock_data.json`: Raw stock data from NSE

## Requirements

- Python 3.x
- pandas
- transformers
- torch
- streamlit
- plotly
- requests
- T5 model: "AventIQ-AI/t5-stockmarket-qa-chatbot"

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install pandas transformers torch streamlit plotly requests
```

## Usage

1. First, fetch the latest stock data:
```bash
python scrapper.py
```

2. Format the data:
```bash
python data_formatting.py
```

3. Launch the web interface:
```bash
streamlit run main_streamlit.py
```

## Features in Detail

### Data Collection
- Automated scraping of NIFTY 50 stock data from NSE India
- Data processing and formatting for analysis
- Support for both JSON and CSV data formats

### Analysis Capabilities
- Real-time price analysis
- Technical indicators
- Performance metrics (daily, monthly, yearly)
- AI-powered insights and recommendations
- Industry-specific analysis

### Visualization
- Interactive charts and graphs
- Performance comparison visualizations
- Price range analysis
- Trading activity metrics

## Input Data Format

The system expects the following data fields:
- symbol
- companyName
- industry (optional)
- open
- dayHigh
- dayLow
- lastPrice
- previousClose
- change
- pChange
- yearHigh
- yearLow
- totalTradedVolume
- totalTradedValue
- perChange365d
- perChange30d

## Output

The analysis provides:
- Basic company information
- Current market position
- Technical analysis
- AI-generated insights
- Performance metrics
- Investment recommendations
- Risk factors

## Note

- The tool uses garbage collection to manage memory efficiently
- Regular data updates are recommended for accurate analysis
- The AI model requires internet connection for initial download

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

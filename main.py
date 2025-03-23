import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, T5ForConditionalGeneration, T5Tokenizer
import torch
import gc

class EnhancedStockAnalyzer:
    def __init__(self):
        gc.collect()

        self.model_name = "AventIQ-AI/t5-stockmarket-qa-chatbot"
        print("Loading model...")
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        print("Model loaded!")
        self.stock_data = None

    def load_stock_data(self, csv_path):
        try:
            self.stock_data = pd.read_csv(csv_path)

            if 'industry' not in self.stock_data.columns:
                self.stock_data['industry'] = 'N/A'

            numeric_columns = ['open', 'dayHigh', 'dayLow', 'lastPrice', 'previousClose',
                             'change', 'pChange', 'yearHigh', 'yearLow', 'totalTradedVolume',
                             'totalTradedValue', 'perChange365d', 'perChange30d']

            for col in numeric_columns:
                if col in self.stock_data.columns:
                    self.stock_data[col] = pd.to_numeric(self.stock_data[col], errors='coerce')

            print(f"Loaded data for {len(self.stock_data)} stocks")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            self.stock_data = pd.DataFrame()

    def generate_key_insights(self, stock) -> dict:
        insights = {
            "growth_metrics": [],
            "valuation_risks": [],
            "technical_signals": [],
            "market_risks": [],
            "strategy": []
        }
        yearly_change = float(stock['perChange365d'])
        monthly_change = float(stock['perChange30d'])
        daily_change = float(stock['pChange'])

        if abs(yearly_change) > 20:
            if yearly_change > 0:
                insights["growth_metrics"].append(f"Strong yearly growth of {yearly_change:.1f}%")
            else:
                insights["growth_metrics"].append(f"Significant yearly decline of {yearly_change:.1f}%")

        if abs(monthly_change) > 10:
            if monthly_change > 0:
                insights["growth_metrics"].append(f"Robust monthly gains: +{monthly_change:.1f}%")
            else:
                insights["growth_metrics"].append(f"Notable monthly decline: {monthly_change:.1f}%")

        current_price = float(stock['lastPrice'])
        year_high = float(stock['yearHigh'])
        year_low = float(stock['yearLow'])
        price_position = (current_price - year_low) / (year_high - year_low) * 100

        if price_position > 80:
            insights["technical_signals"].append("Trading near 52-week high")
            insights["valuation_risks"].append("Potential overvaluation risk at current levels")
        elif price_position < 20:
            insights["technical_signals"].append("Trading near 52-week low")
            insights["strategy"].append("Consider gradual accumulation at these levels")

        value_cr = float(stock['totalTradedValue'])/10000000
        if value_cr > 1000:
            insights["technical_signals"].append(f"High trading activity: ₹{value_cr:.0f}Cr")

        if price_position > 90:
            insights["market_risks"].append("Overbought conditions - higher risk of pullback")
            insights["strategy"].append("Consider booking partial profits")
        elif price_position < 10:
            insights["market_risks"].append("Oversold conditions - watch for reversal")
            insights["strategy"].append("Opportunity for value investors")

        if abs(daily_change) > 3:
            insights["technical_signals"].append(f"High volatility: {daily_change:+.1f}% today")
            insights["strategy"].append("Use stop-loss for risk management")

        industry = stock['industry'] if 'industry' in stock else None
        if pd.notna(industry):
            insights["market_risks"].append(f"Monitor {industry} sector trends and competition")

        return insights

    def analyze_stock(self, symbol: str) -> dict:
        if self.stock_data is None or self.stock_data.empty:
            return {"error": "No data loaded"}

        try:
            stock = self.stock_data[self.stock_data['symbol'] == symbol].iloc[0]

            yearly_change = float(stock['perChange365d'])
            monthly_change = float(stock['perChange30d'])
            daily_change = float(stock['pChange'])
            current_price = float(stock['lastPrice'])
            year_high = float(stock['yearHigh'])
            year_low = float(stock['yearLow'])
            price_position = (current_price - year_low) / (year_high - year_low) * 100
            value_cr = float(stock['totalTradedValue'])/10000000

            insights = {
                "growth": {
                    "icon": "✅",
                    "title": "Growth Analysis",
                    "details": []
                },
                "valuation": {
                    "icon": "⚠️",
                    "title": "Valuation Risk",
                    "details": []
                },
                "technical": {
                    "icon": "📈",
                    "title": "Technical Indicators",
                    "details": []
                },
                "market": {
                    "icon": "🌍",
                    "title": "Market Risks",
                    "details": []
                },
                "strategy": {
                    "icon": "💡",
                    "title": "Investment Strategy",
                    "details": []
                }
            }

            if yearly_change > 20:
                insights["growth"]["details"].append(f"Strong yearly growth of {yearly_change:.1f}%")
            elif yearly_change < -20:
                insights["growth"]["details"].append(f"Significant decline of {yearly_change:.1f}%")
            if monthly_change > 10:
                insights["growth"]["details"].append(f"Robust monthly performance: +{monthly_change:.1f}%")
            if not insights["growth"]["details"]:
                insights["growth"]["details"].append(f"Moderate growth with {yearly_change:.1f}% yearly change")

            if price_position > 80:
                insights["valuation"]["details"].append("Trading near 52-week high, potential overvaluation")
            elif price_position < 20:
                insights["valuation"]["details"].append("Trading near 52-week low, possible undervaluation")
            else:
                insights["valuation"]["details"].append(f"Trading at {price_position:.1f}% of 52-week range")

            if price_position > 90:
                insights["technical"]["details"].append("Strongly overbought conditions")
            elif price_position < 10:
                insights["technical"]["details"].append("Strongly oversold conditions")
            if value_cr > 1000:
                insights["technical"]["details"].append(f"High trading activity: ₹{value_cr:.0f}Cr")
            if not insights["technical"]["details"]:
                insights["technical"]["details"].append("Neutral technical indicators")

            industry = stock['industry'] if 'industry' in stock else 'N/A'
            insights["market"]["details"].append(f"Monitor {industry} sector trends")
            if abs(daily_change) > 3:
                insights["market"]["details"].append(f"High volatility: {daily_change:+.1f}% daily change")

            if price_position > 80:
                insights["strategy"]["details"].append("Consider profit booking or staggered exit")
            elif price_position < 20:
                insights["strategy"]["details"].append("Opportunity for gradual accumulation")
            else:
                insights["strategy"]["details"].append("Hold with strict stop-loss")

            insight_prompt = f"""Question: Provide a detailed analysis for {symbol} ({stock['companyName']}) in the {industry} sector:

Current Market Data:
• Price: ₹{current_price:,.2f} ({daily_change:+.2f}% today)
• 52-Week Range: ₹{year_low:,.2f} - ₹{year_high:,.2f}
• Trading Value: ₹{value_cr:,.2f}Cr
• Price Position: {price_position:.1f}% of 52-week range

Performance Changes:
• Daily: {daily_change:+.2f}%
• Monthly: {monthly_change:+.2f}%
• Yearly: {yearly_change:+.2f}%

Technical Analysis:
• Growth: {', '.join(insights['growth']['details'])}
• Valuation: {', '.join(insights['valuation']['details'])}
• Technical Indicators: {', '.join(insights['technical']['details'])}
• Market Risks: {', '.join(insights['market']['details'])}
• Strategy: {', '.join(insights['strategy']['details'])}

Provide a structured analysis with the following sections:
1. Overall Market Position: Current standing and momentum
2. Key Strengths: Positive factors and opportunities
3. Primary Concerns: Risk factors and challenges
4. Investment Recommendations: Clear actionable steps
5. Risk Monitoring: Specific factors to watch

Answer: """

            # geneRating analysis using the model
            inputs = self.tokenizer(insight_prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=300,  # can be increased depending how detailed analysis you desire
                num_beams=5,
                temperature=0.7,
                no_repeat_ngram_size=3,
                top_k=50,
                top_p=0.95,
                early_stopping=True
            )
            ai_analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            return {
                "basic_info": {
                    "symbol": symbol,
                    "company": stock['companyName'] if 'companyName' in stock else symbol,
                    "industry": industry
                },
                "price_data": {
                    "current_price": current_price,
                    "day_range": {"low": float(stock['dayLow']), "high": float(stock['dayHigh'])},
                    "year_range": {"low": year_low, "high": year_high}
                },
                "performance": {
                    "daily_change": daily_change,
                    "monthly_change": monthly_change,
                    "yearly_change": yearly_change
                },
                "trading_info": {
                    "volume": int(stock['totalTradedVolume']),
                    "value_cr": value_cr
                },
                "insights": insights,
                "ai_analysis": ai_analysis
            }

        except Exception as e:
            return {"error": str(e)}
        finally:
            gc.collect()
"""
Multi-Ticker Price & Dividend Agent — HTML Output
"""
# Install yfinance if not already installed
#pip install yfinance -q

import yfinance as yf
import pandas as pd
from datetime import datetime
from IPython.display import display, HTML

def fetch_ticker_data(symbol):
    """Fetch price and dividend data for a single ticker."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="5d")

        if history.empty:
            return None

        latest = history.iloc[-1]
        prev_close = history.iloc[-2]["Close"] if len(history) > 1 else None

        change = latest["Close"] - prev_close if prev_close else 0
        change_pct = (change / prev_close * 100) if prev_close else 0

        return {
            "Symbol": symbol,
            "Name": info.get("shortName", "N/A"),
            "Price": latest["Close"],
            "Change": change,
            "Change %": change_pct,
            "Open": latest["Open"],
            "High": latest["High"],
            "Low": latest["Low"],
            "Volume": latest["Volume"],
            "Div Yield %": (info.get("dividendYield") or 0),
            "Div Rate $/yr": info.get("dividendRate", 0) or 0,
        }
    except Exception as e:
        print(f"  ⚠ Error fetching {symbol}: {e}")
        return None


def build_html_table(df):
    """Build a styled HTML table from the dataframe."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows_html = ""
    for _, row in df.iterrows():
        change_color = "#16a34a" if row["Change %"] >= 0 else "#dc2626"
        change_icon = "▲" if row["Change %"] >= 0 else "▼"
        yield_color = "#16a34a" if row["Div Yield %"] >= 5 else "#2563eb"

        rows_html += f"""
        <tr>
            <td style="font-weight:700; color:#1e293b;">{row['Symbol']}</td>
            <td style="color:#475569;">{row['Name']}</td>
            <td style="font-weight:600;">${row['Price']:.2f}</td>
            <td style="color:{change_color}; font-weight:600;">
                {change_icon} ${abs(row['Change']):.2f} ({row['Change %']:+.2f}%)
            </td>
            <td style="text-align:right;">${row['Open']:.2f}</td>
            <td style="text-align:right;">${row['High']:.2f}</td>
            <td style="text-align:right;">${row['Low']:.2f}</td>
            <td style="text-align:right;">{row['Volume']:,.0f}</td>
            <td style="font-weight:700; color:{yield_color}; text-align:center;">
                {row['Div Yield %']:.2f}%
            </td>
            <td style="text-align:right;">${row['Div Rate $/yr']:.2f}</td>
        </tr>"""

    # Summary row
    avg_yield = df["Div Yield %"].mean()
    avg_price = df["Price"].mean()

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px;">
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white;
                    padding: 20px 28px; border-radius: 12px 12px 0 0;">
            <h2 style="margin:0 0 4px 0; font-size:20px;">📊 Dividend & Price Tracker</h2>
            <p style="margin:0; opacity:0.8; font-size:13px;">
                {len(df)} tickers · Updated {timestamp}
            </p>
        </div>

        <div style="overflow-x: auto; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
            <table style="width:100%; border-collapse:collapse; font-size:14px;">
                <thead>
                    <tr style="background:#f1f5f9;">
                        <th style="padding:12px 16px; text-align:left; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Symbol</th>
                        <th style="padding:12px 16px; text-align:left; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Name</th>
                        <th style="padding:12px 16px; text-align:left; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Price</th>
                        <th style="padding:12px 16px; text-align:left; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Change</th>
                        <th style="padding:12px 16px; text-align:right; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Open</th>
                        <th style="padding:12px 16px; text-align:right; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">High</th>
                        <th style="padding:12px 16px; text-align:right; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Low</th>
                        <th style="padding:12px 16px; text-align:right; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Volume</th>
                        <th style="padding:12px 16px; text-align:center; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Div Yield</th>
                        <th style="padding:12px 16px; text-align:right; color:#64748b; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">Div Rate</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
                <tfoot>
                    <tr style="background:#f8fafc; border-top: 2px solid #e2e8f0;">
                        <td colspan="2" style="padding:12px 16px; font-weight:700; color:#64748b;">AVERAGES</td>
                        <td style="padding:12px 16px; font-weight:600;">${avg_price:.2f}</td>
                        <td colspan="5"></td>
                        <td style="padding:12px 16px; font-weight:700; text-align:center; color:#2563eb;">{avg_yield:.2f}%</td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>

        <div style="margin-top:16px; display:flex; gap:12px; flex-wrap:wrap;">
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px 18px; flex:1; min-width:200px;">
                <div style="font-size:12px; color:#16a34a; font-weight:600;">HIGHEST YIELD</div>
                <div style="font-size:20px; font-weight:700; color:#15803d;">
                    {df.loc[df['Div Yield %'].idxmax(), 'Symbol']} — {df['Div Yield %'].max():.2f}%
                </div>
            </div>
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:12px 18px; flex:1; min-width:200px;">
                <div style="font-size:12px; color:#2563eb; font-weight:600;">HIGHEST PRICE</div>
                <div style="font-size:20px; font-weight:700; color:#1d4ed8;">
                    {df.loc[df['Price'].idxmax(), 'Symbol']} — ${df['Price'].max():.2f}
                </div>
            </div>
            <div style="background:#fefce8; border:1px solid #fef08a; border-radius:8px; padding:12px 18px; flex:1; min-width:200px;">
                <div style="font-size:12px; color:#ca8a04; font-weight:600;">PORTFOLIO AVG YIELD</div>
                <div style="font-size:20px; font-weight:700; color:#a16207;">
                    {avg_yield:.2f}%
                </div>
            </div>
        </div>
    </div>
    """
    return html


def run_agent(tickers):
    """Fetch data for all tickers and display as HTML."""
    print(f"Fetching data for {len(tickers)} tickers...\n")

    results = []
    for symbol in tickers:
        print(f"  Fetching {symbol}...", end=" ")
        data = fetch_ticker_data(symbol)
        if data:
            print(f"✓ ${data['Price']:.2f}")
            results.append(data)
        else:
            print("✗ Failed")

    if not results:
        print("\nNo data retrieved. Check your tickers and try again.")
        return None

    df = pd.DataFrame(results)
    html = build_html_table(df)
    display(HTML(html))

    #
    print(f"\nTip: Data is stored in the 'df' variable. Try: df.sort_values('Div Yield %', ascending=False)")
    return df

TICKERS = ["AGNC","HYT","NLY","MAIN","JEPI"]

# --- RUN ---
df = run_agent(TICKERS)

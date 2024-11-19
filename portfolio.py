# economics, portfolio management
# IMF data https://data.imf.org/?sk=388dfa60-1d26-4ade-b505-a05a558d9a42

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
import threading
import time


class IBKRClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.account_summary = {}
        self.portfolio_data = []

    def error(self, reqId, errorCode, errorString):
        print(f"Error {reqId}: {errorCode} - {errorString}")

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        print(f"Next valid order ID: {self.nextOrderId}")
        # Request account summary after connection is established
        self.reqAccountSummary(9001, "All", "NetLiquidation,TotalCashBalance")

    def accountSummary(self, reqId, account, tag, value, currency):
        # Store account summary data
        self.account_summary[tag] = value
        print(f"Account Summary - {tag}: {value} {currency}")

    def accountSummaryEnd(self, reqId):
        print("Account Summary Received.")

    def updatePortfolio(self, contract, position, marketPrice, marketValue,
                        averageCost, unrealizedPNL, realizedPNL, accountName):
        # Store portfolio data
        self.portfolio_data.append({
            "Symbol": contract.symbol,
            "Position": position,
            "Market Price": marketPrice,
            "Market Value": marketValue,
            "Average Cost": averageCost,
            "Unrealized PNL": unrealizedPNL,
            "Realized PNL": realizedPNL,
        })
        print(f"Portfolio Update - {contract.symbol}: {position} shares at {marketPrice} USD.")

    def accountDownloadEnd(self, accountName):
        print(f"Portfolio Download Complete for Account: {accountName}")


def run_loop(client):
    client.run()

import matplotlib.pyplot as plt
import pandas as pd

class PortfolioVisualizer:
    def __init__(self, style="ggplot"):
        # Initialize with a default style
        plt.style.use(style)
        self.style = style

    def plot_portfolio_value(self, data, title="Portfolio Value Over Time"):
        """
        Line chart for portfolio value over time.
        Args:
            data (pd.DataFrame): DataFrame with 'Date' and 'Value' columns.
            title (str): Chart title.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(data["Date"], data["Value"], label="Portfolio Value", marker="o")
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Value (USD)")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_asset_allocation(self, allocations, title="Asset Allocation"):
        """
        Pie chart for asset allocation.
        Args:
            allocations (dict): Dictionary with asset names as keys and percentages as values.
            title (str): Chart title.
        """
        labels = allocations.keys()
        sizes = allocations.values()
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title(title)
        plt.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
        plt.show()

    def plot_unrealized_pnl(self, data, title="Unrealized P&L"):
        """
        Bar chart for unrealized P&L by asset using matplotlib.
        Args:
            data (pd.DataFrame): DataFrame with 'Asset' and 'Unrealized P&L' columns.
            title (str): Chart title.
        """
        plt.figure(figsize=(10, 6))
        plt.bar(data["Asset"], data["Unrealized P&L"], color="dodgerblue", edgecolor="black")
        plt.title(title)
        plt.xlabel("Asset")
        plt.ylabel("Unrealized P&L (USD)")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    def interactive_portfolio_value(self, data, title="Portfolio Value Over Time"):
        """
        Interactive line chart using Plotly.
        Args:
            data (pd.DataFrame): DataFrame with 'Date' and 'Value' columns.
            title (str): Chart title.
        """
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Date"], y=data["Value"],
                                 mode="lines+markers",
                                 name="Portfolio Value"))
        fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Value (USD)")
        fig.show()

if __name__ == "__main__":
    # Create the client
    app = IBKRClient()

    # Connect to TWS or IB Gateway
    app.connect("127.0.0.1", 7497, clientId=1)  # Use port 7496 for live accounts

    # Start the API thread
    api_thread = threading.Thread(target=run_loop, args=(app,), daemon=True)
    api_thread.start()

    # Allow time to connect and request data
    time.sleep(2)

    # Request portfolio data
    app.reqAccountUpdates(True, "")  # "" requests updates for all accounts

    # Allow time for data retrieval
    time.sleep(10)

    # Print portfolio data
    print("\nPortfolio Summary:")
    for item in app.portfolio_data:
        print(item)

    # Disconnect
    app.disconnect()

# Financial analysis for yfinance stocks

class Company:
    def __init__(self, name, financials):
        """
        Initialize the company with its financial data.
        :param name: str: Name of the company
        :param financials: dict: Financial data (e.g., 'Net Income', 'Total Debt', etc.)
        """
        self.name = name
        self.financials = financials

    # === Profitability Metrics ===
    class ProfitabilityMetrics:
        def __init__(self, financials):
            self.financials = financials

        def eps(self):
            """Earnings Per Share = (Net Income - Preferred Dividends) / Common Shares Outstanding"""
            try:
                return (self.financials['Net Income'] - self.financials.get('Preferred Stock Dividends', 0)) / self.financials['Basic Average Shares']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def roe(self):
            """Return on Equity = Net Income / Average Equity
            Assume common shareholders' equity 
            Common equity includes: common stock, retained earnings, additional paid-in capital. 
            Not preferred equity or minor interest
            Using the average ensures the equity base is representative of the entire period.
            Common mistakes: 
            1. Not adjusting for preferred dividends when preferred stock exists can misstate ROE.
            2. Using total equity instead of common equity leads to inflated or inaccurate ROE.
            3. Using only the ending equity figure can distort the results, especially if equity fluctuates during the period.
            """
            average_equity = (self.financials['Common Stock Equity'].values[0] + self.financials['Common Stock Equity'].values[1]) / 2
            try:
                return self.financials['Net Income'] / average_equity
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def gross_margin(self):
            """Gross Margin = (Revenue - Cost of Revenue) / Revenue
            1. Incorrect revenue / COGS. Ensure that COGS only includes direct costs (e.g., materials, labor) and excludes operating expenses like rent or marketing.
            2. Negative value. This can occur if COGS exceeds revenue, indicating unsustainable pricing or production inefficiencies.
            """
            try:
                return (self.financials['Total Revenue'] - self.financials['Reconciled Cost Of Revenue']) / self.financials['Total Revenue']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def net_margin(self):
            """Net Margin = Net Income / Total Revenue"""
            try:
                return self.financials['Net Income'] / self.financials['Total Revenue']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

    # === Liquidity Metrics ===
    class LiquidityMetrics:
        def __init__(self, financials):
            self.financials = financials

        def current_ratio(self):
            """Current Ratio = Current Assets / Current Liabilities"""
            try:
                return self.financials['Current Assets'] / self.financials['Current Liabilities']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def quick_ratio(self):
            """Quick Ratio = (Current Assets - Inventory) / Current Liabilities"""
            try:
                return (self.financials['Current Assets'] - self.financials['Inventory']) / self.financials['Current Liabilities']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def cash_ratio(self):
            """Cash Ratio = Cash / Current Liabilities"""
            try:
                return self.financials['Cash And Cash Equivalents'] / self.financials['Current Liabilities']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

    # === Solvency Metrics ===
    class SolvencyMetrics:
        def __init__(self, financials):
            self.financials = financials

        def debt_to_equity(self):
            """Debt-to-Equity Ratio = Total Debt / Total Equity"""
            try:
                return self.financials['Total Debt'] / self.financials['Stockholders Equity']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def interest_coverage(self):
            """Interest Coverage Ratio = EBIT / Interest Expense"""
            try:
                return self.financials['EBIT'] / self.financials['Interest Expense']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def financial_leverage(self):
            """Financial Leverage = Total Assets / Total Equity"""
            try:
                return self.financials['Total Assets'] / self.financials['Stockholders Equity']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

    # === Efficiency Metrics ===
    class EfficiencyMetrics:
        def __init__(self, financials):
            self.financials = financials

        def inventory_turnover(self):
            """Inventory Turnover = Cost of Goods Sold / Average Inventory"""
            try:
                return self.financials['Reconciled Cost of Revenue'] / self.financials['Average Inventory']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def asset_turnover(self):
            """Asset Turnover = Total Revenue / Total Assets"""
            try:
                return self.financials['Total Revenue'] / self.financials['Total Assets']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def receivables_turnover(self):
            """Receivables Turnover = Total Revenue / Average Receivables"""
            average_receivables = (self.financials['Receivables'].values[0] + self.financials['Receivables'].values[1]) / 2
            try:
                return self.financials['Total Revenue'] / average_receivables
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

    # === Valuation Metrics ===
    class ValuationMetrics:
        def __init__(self, financials):
            self.financials = financials

        def price_to_earnings(self):
            """P/E Ratio = Market Price per Share / EPS"""
            try:
                eps = (self.financials['Net Income'] - self.financials.get('Preferred Stock Dividends', 0)) / self.financials['Basic Average Shares']
                return self.financials['Market Price Per Share'] / eps
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def price_to_book(self):
            """P/B Ratio = Market Price per Share / (Total Equity / Basic Shares Outstanding)"""
            try:
                book_value_per_share = self.financials['Stockholders Equity'] / self.financials['Basic Average Shares']
                return self.financials['Market Price Per Share'] / book_value_per_share
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

        def ev_to_ebitda(self):
            """EV/EBITDA = (Market Cap + Total Debt - Cash) / EBITDA"""
            market_cap = self.financials['Market Price Per Share'] * self.financials['Basic Average Shares']
            try:
                enterprise_value = market_cap + self.financials['Total Debt'] - self.financials['Cash And Cash Equivalents']
                return enterprise_value / self.financials['Normalized EBITDA']
            except (KeyError, ZeroDivisionError) as e:
                return f"Error: {e}"

    def calculate_metrics(self):
        """
        Calculates all metrics and organizes results.
        """
        return {
            "Profitability": self.ProfitabilityMetrics(self.financials).__dict__,
            "Liquidity": self.LiquidityMetrics(self.financials).__dict__,
            "Efficiency": self.EfficiencyMetrics(self.financials).__dict__,
            "Valuation": self.ValuationMetrics(self.financials).__dict__,
        }

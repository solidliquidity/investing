# FRA
# https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm#ia96e4fb0476549c99dc3a2b2368f643f_343

class Company:
    def __init__(self, name, financials):
        """
        Initialize the company with its financial data.
        :param name: str: Name of the company
        :param financials: dict: Financial data (e.g., net_income, total_debt, etc.)
        """
        self.name = name
        self.financials = financials

    class ProfitabilityMetrics:
        @staticmethod
        def eps(financials):
            return (financials['net_income'] - financials['preferred_dividends']
                    ) / financials['common_shares_outstanding']

        @staticmethod
        def roe(financials):
            return financials['net_income'] / financials['average_equity']

    class LiquidityMetrics:
        @staticmethod
        def current_ratio(financials):
            return financials['current_assets'] / \
                financials['current_liabilities']

        @staticmethod
        def quick_ratio(financials):
            return (financials['current_assets'] - financials['inventory']
                    ) / financials['current_liabilities']

    class SolvencyMetrics:
        @staticmethod
        def debt_to_equity(financials):
            return financials['total_debt'] / financials['total_equity']

        @staticmethod
        def interest_coverage(financials):
            return financials['ebit'] / financials['interest_expense']

    class EfficiencyMetrics:
        @staticmethod
        def inventory_turnover(financials):
            return financials['cogs'] / financials['average_inventory']

    class ValuationMetrics:
        @staticmethod
        def price_to_earnings(financials):
            eps = (financials['net_income'] - financials['preferred_dividends']
                   ) / financials['common_shares_outstanding']
            return financials['market_price_per_share'] / eps

    def calculate_metrics(self):
        """
        Calculates all metrics and organizes results.
        """
        results = {
            "EPS": self.ProfitabilityMetrics.eps(self.financials),
            "ROE": self.ProfitabilityMetrics.roe(self.financials),
            "Current Ratio": self.LiquidityMetrics.current_ratio(self.financials),
            "Quick Ratio": self.LiquidityMetrics.quick_ratio(self.financials),
            "Debt-to-Equity Ratio": self.SolvencyMetrics.debt_to_equity(self.financials),
            "Interest Coverage Ratio": self.SolvencyMetrics.interest_coverage(self.financials),
            "Inventory Turnover": self.EfficiencyMetrics.inventory_turnover(self.financials),
            "P/E Ratio": self.ValuationMetrics.price_to_earnings(self.financials),
        }
        return results

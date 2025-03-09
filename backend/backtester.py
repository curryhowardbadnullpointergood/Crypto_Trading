from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TradeExecution:
    timestamp: datetime
    token: str
    action: str
    quantity: float
    price: float
    # Removed slippage and fees for simplicity

@dataclass
class PortfolioState:
    cash: float
    token_balances: Dict[str, float]
    total_value: float # Simplified, directly track total value
    timestamp: datetime

class CryptoBacktesterSimplified:
    def __init__(
        self,
        agent, # Keep agent for decision making logic (even if simplified)
        trading_pairs: List[str],
        start_date: datetime,
        end_date: datetime,
        initial_capital: float,
        data_tools # Keep data_tools for price data fetching
    ):
        self.agent = agent
        self.trading_pairs = trading_pairs
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.data_tools = data_tools # Assume agent and backtester still need to get data
        # Removed slippage_model

        # Initialize portfolio
        self.portfolio = {
            "cash": initial_capital,
            "tokens": {pair: 0 for pair in trading_pairs}
        }
        self.portfolio_history: List[PortfolioState] = []
        self.trades_history: List[TradeExecution] = []

    async def execute_trade(
        self,
        token: str,
        action: str,
        quantity: float,
        current_price: float
    ) -> Optional[TradeExecution]:
        """Simplified trade execution without slippage and fees."""
        if quantity <= 0:
            return None

        executed_price = current_price # No slippage

        if action == "buy":
            total_cost = quantity * executed_price
            if total_cost <= self.portfolio["cash"]:
                self.portfolio["cash"] -= total_cost
                self.portfolio["tokens"][token] += quantity
                return TradeExecution(
                    timestamp=datetime.now(),
                    token=token,
                    action=action,
                    quantity=quantity,
                    price=executed_price,
                    # Removed slippage=0, fees=0
                )
        elif action == "sell":
            if quantity <= self.portfolio["tokens"][token]:
                revenue = quantity * executed_price
                self.portfolio["cash"] += revenue
                self.portfolio["tokens"][token] -= quantity
                return TradeExecution(
                    timestamp=datetime.now(),
                    token=token,
                    action=action,
                    quantity=quantity,
                    price=executed_price,
                    # Removed slippage=0, fees=0
                )
        return None

    async def run_backtest(self):
        """Simplified backtest simulation."""
        dates = [self.start_date + timedelta(hours=i) for i in range(int((self.end_date - self.start_date).total_seconds() / 3600) + 1)]

        print("\nStarting simplified crypto backtest...")
        print(f"{'Date':<20} {'Token':<10} {'Action':<6} {'Quantity':>10} {'Price':>10} {'Portfolio Value':>15}")
        print("-" * 75)

        for current_date in dates:
            market_state = {}
            for token in self.trading_pairs:
                metrics = await self.data_tools.get_token_metrics(token) # Assume agent still needs price data
                market_state[token] = {
                    "price": metrics.price,
                }

            decisions = await self.agent.generate_trading_signals( # Agent still makes decisions
                market_state=market_state,
                portfolio=self.portfolio
            )

            for token, decision in decisions.items():
                trade_execution = await self.execute_trade(
                    token=token,
                    action=decision["action"],
                    quantity=decision["quantity"],
                    current_price=market_state[token]["price"]
                )

                if trade_execution:
                    self.trades_history.append(trade_execution)
                    # Removed detailed trade print for extreme simplification
                    # print(f"Trade executed: {trade_execution}")

            # Update portfolio state
            total_value = self.portfolio["cash"]
            for token in self.trading_pairs:
                total_value += self.portfolio["tokens"][token] * market_state[token]["price"]

            self.portfolio_history.append(
                PortfolioState(
                    cash=self.portfolio["cash"],
                    token_balances=self.portfolio["tokens"].copy(),
                    total_value=total_value,
                    timestamp=current_date
                )
            )
            print(f"{current_date:%Y-%m-%d %H:%M} Portfolio Value: {total_value:>15.2f}") # Simplified output


    def analyze_performance(self):
        """Simplified performance analysis - just total return."""
        if not self.portfolio_history:
            return None

        start_value = self.initial_capital
        end_value = self.portfolio_history[-1].total_value
        total_return = (end_value - start_value) / start_value

        print("\nSimplified Performance Metrics:")
        print(f"Total Return: {total_return:.2%}")

        return total_return # Return total return value

if __name__ == "__main__":
    # Simplified example usage, hardcoded parameters
    from tools import CryptoDataTools  # Assume tools and agent are still needed in simplified version
    from agents import SimpleTradingAgent as Agent # Assuming a simplified agent

    trading_pairs = ['SOL', 'BONK', 'JUP']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7) # Shorter backtest period
    initial_capital = 1000

    data_tools = CryptoDataTools() # Initialize data tools (assume still necessary)
    backtester = CryptoBacktesterSimplified(
        agent=Agent(), # Use a simplified agent
        trading_pairs=trading_pairs,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        data_tools=data_tools # Pass data tools
    )

    import asyncio
    asyncio.run(backtester.run_backtest())
    performance_return = backtester.analyze_performance() # Get return value
    if performance_return is not None:
        print(f"Backtest completed, total return: {performance_return:.2%}")
    else:
        print("Backtest did not generate performance data.")
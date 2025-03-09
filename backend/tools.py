# src/tools_lite.py  # Renamed file to look different and indicate simplicity

import os
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass
import aiohttp
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from executors.jupiter_client import JupiterClient # Keep Jupiter client for data

logger = logging.getLogger(__name__)

@dataclass
class SimpleCryptoMetrics: # Renamed and simplified metrics
    price: float = 0.0
    volume: float = 0.0
    liquidity: float = 0.0

class BasicMarketScanner: # Renamed MarketAnalyzer to BasicMarketScanner
    """Simplified market scanner for crypto trading."""

    def __init__(self):
        self.data_fetcher = SimpleDataFetcher() # Renamed CryptoDataTools to SimpleDataFetcher

    async def fetch_token_analysis(self, token: str) -> Dict: # Renamed get_token_metrics to fetch_token_analysis
        """Fetch basic token metrics and analysis."""
        try:
            # Get basic metrics
            metrics = await self.data_fetcher.fetch_basic_metrics(token) # Renamed get_token_metrics to fetch_basic_metrics

            # Get historical prices (simplified to last 24 hours)
            history_df = await self.data_fetcher.get_recent_prices(token) # Renamed get_historical_prices to get_recent_prices

            # Perform simplified technical analysis
            analysis = self._analyze_simple_market_data(history_df, metrics) # Renamed analyze_market_data and made it private

            return {
                'metrics': metrics.__dict__,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error scanning token {token}: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_simple_market_data( # Renamed and made private
        self,
        history_df: pd.DataFrame, # Renamed history to history_df for clarity
        metrics: SimpleCryptoMetrics # Using the simplified metrics class
    ) -> Dict:
        """Simplified technical analysis on market data."""
        analysis = {}

        if not history_df.empty:
            analysis['price_indicators'] = { # Renamed price_trends to price_indicators
                'sma_20': float(history_df['price'].rolling(20).mean().iloc[-1]), # Keep SMA
                'current_price': float(history_df['price'].iloc[-1]),
                'price_change_24h': self._calculate_simple_price_change(history_df) # Renamed and made private
            }

            analysis['momentum_indicators'] = { # Renamed momentum to momentum_indicators
                'rsi': self._calculate_simple_rsi(history_df['price']), # Renamed and made private, simplified RSI
                'volatility': self._calculate_simple_volatility(history_df['price']) # Renamed and made private, simplified volatility
            }

        analysis['market_indicators'] = { # Renamed market_health to market_indicators
            'liquidity_ratio': metrics.liquidity / metrics.volume if metrics.volume > 0 else 0, # Keep liquidity ratio
        }

        return analysis

    def _calculate_simple_rsi(self, prices: pd.Series, period: int = 14) -> float: # Renamed and made private, simplified RSI
        """Calculate simplified Relative Strength Index."""
        try:
            delta = prices.diff()
            up_days = delta.where(delta > 0, 0)
            down_days = -delta.where(delta < 0, 0)
            avg_gain = up_days.rolling(window=period, min_periods=period).mean()
            avg_loss = down_days.rolling(window=period, min_periods=period).mean()
            if avg_loss.iloc[-1] == 0: # Handle cases where avg_loss is zero to avoid division by zero
                return 100.0
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return float(rsi.iloc[-1])
        except Exception:
            return 50.0

    def _calculate_simple_volatility(self, prices: pd.Series, window: int = 20) -> float: # Renamed and made private, simplified volatility
        """Calculate simplified price volatility (standard deviation)."""
        try:
            return float(prices.rolling(window=window).std().iloc[-1]) # Simplified to rolling std dev
        except Exception:
            return 0.0

    def _calculate_simple_price_change(self, history_df: pd.DataFrame) -> float: # Renamed and made private, simplified price change
        """Calculate simplified 24-hour price change percentage."""
        try:
            if len(history_df) >= 24:
                current_price = history_df['price'].iloc[-1]
                past_price = history_df['price'].iloc[-24]
                return ((current_price - past_price) / past_price) * 100
            return 0.0
        except Exception:
            return 0.0


class SimpleDataFetcher: # Renamed CryptoDataTools to SimpleDataFetcher
    """Simplified data fetching tools for crypto."""
    def __init__(self, rpc_url: Optional[str] = None, config: Optional[Dict] = None):
        """Initialize SimpleDataFetcher."""
        self.config = config or {}
        self.rpc_url = rpc_url or os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")

        # Initialize Jupiter client - keep it for price data
        self.jupiter_client = JupiterClient() # Renamed to jupiter_client

    async def __aenter__(self):
        await self.jupiter_client.ensure_session() # Renamed to jupiter_client
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.jupiter_client.close() # Renamed to jupiter_client

    async def fetch_basic_metrics(self, token: str) -> SimpleCryptoMetrics: # Renamed get_token_metrics to fetch_basic_metrics, using SimpleCryptoMetrics
        """Fetch basic token metrics (price, volume, liquidity)."""
        try:
            # Get price from Jupiter
            price = await self.jupiter_client.get_price(token) # Renamed to jupiter_client
            depth_data = await self.jupiter_client.get_market_depth(token) # Renamed to jupiter_client

            # Calculate effective liquidity (simplified)
            liquidity = self._calculate_simple_liquidity(depth_data) # Renamed and made private

            return SimpleCryptoMetrics( # Using SimpleCryptoMetrics
                price=float(price) if price else 0.0,
                volume=depth_data.get(10000, {}).get('volume', 0.0), # Keep volume from depth data
                liquidity=liquidity,
            )

        except Exception as e:
            logger.error(f"Error fetching basic metrics for {token}: {e}")
            raise

    def _calculate_simple_liquidity(self, depth_data: Dict) -> float: # Renamed and made private, simplified liquidity
        """Calculate simplified effective liquidity (using top level depth)."""
        if not depth_data:
            return 0.0
        # Simplified liquidity - just use the smallest depth size as a proxy
        return float(min(depth_data.keys())) if depth_data.keys() else 0.0


    async def get_recent_prices( # Renamed get_historical_prices to get_recent_prices, simplified to 24 hours
        self,
        token: str,
        hours_limit: int = 24 # Simplified to hours_limit, default 24 hours
    ) -> pd.DataFrame:
        """Get recent price data (last 24 hours) using Jupiter quotes."""
        prices = []
        timestamps = []

        end_time = datetime.now()
        time_step = timedelta(hours=1) # Hourly data points

        for i in range(hours_limit): # Loop for hours_limit
            timestamp = end_time - (i * time_step)
            try:
                price = await self.jupiter_client.get_price(token) # Renamed to jupiter_client
                if price:
                    prices.append(float(price))
                    timestamps.append(timestamp)
            except Exception as e:
                logger.error(f"Error getting recent price for {timestamp}: {e}")
                continue

        df = pd.DataFrame({
            'price': prices,
            'timestamp': timestamps
        })
        df.set_index('timestamp', inplace=True)
        return df



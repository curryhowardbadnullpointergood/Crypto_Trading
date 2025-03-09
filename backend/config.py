# src/config.py
import os
from dataclasses import dataclass

@dataclass
class SimpleChainConfig:
    chain_id: str = "solana" # Default to Solana
    name: str = "Solana"
    rpc_url: str = "https://api.mainnet-beta.solana.com" # Default Solana RPC
    native_token: str = "SOL"
    explorer_url: str = "https://solscan.io"

@dataclass
class SimpleLLMConfig:
    provider: str = "openai" # Default to OpenAI
    model: str = "gpt-3.5-turbo" # Choose a simpler model by default
    api_key: str = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_API_KEY") # Keep API key from env for security, add placeholder
    temperature: float = 0.7

@dataclass
class SimpleTradingConfig:
    max_position_size: float = 10000 # Example default
    risk_tolerance: float = 0.7 # Example default
    min_confidence: float = 0.7 # Example default
    slippage_tolerance: float = 0.01 # Example default

@dataclass
class SimpleDEXConfig:
    api_url: str = "https://quote-api.jup.ag/v6" # Default to Jupiter API

class SimpleConfig:
    # Use direct instances of the dataclasses, simpler than dictionaries
    CHAIN = SimpleChainConfig()
    LLM = SimpleLLMConfig()
    TRADING = SimpleTradingConfig()
    DEX = SimpleDEXConfig()

    # No need for get_* methods in a simple config, access attributes directly
    # e.g., SimpleConfig.CHAIN.rpc_url
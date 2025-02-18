# config.py – Configuration file for API keys, wallets, and settings

### CEX API KEYS ###
CEX_CONFIG = {
    "binance": {
        "api_key": "YOUR_BINANCE_API_KEY",
        "api_secret": "YOUR_BINANCE_API_SECRET"
    },
    "kucoin": {
        "api_key": "YOUR_KUCOIN_API_KEY",
        "api_secret": "YOUR_KUCOIN_API_SECRET",
        "passphrase": "YOUR_KUCOIN_PASSPHRASE"
    }
}

### DEX SETTINGS ###
DEX_CONFIG = {
    "ethereum": {
        "rpc_url": "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
        "wallet_address": "YOUR_WALLET_ADDRESS",
        "private_key": "YOUR_PRIVATE_KEY"
    },
    "bsc": {
        "rpc_url": "https://bsc-dataseed.binance.org/",
        "wallet_address": "YOUR_WALLET_ADDRESS",
        "private_key": "YOUR_PRIVATE_KEY"
    }
}

### GENERAL SETTINGS ###
TRADE_SETTINGS = {
    "min_profit_threshold": 0.5,  # Minimum profit % required for arbitrage
    "trade_amount": 100,  # Amount per trade in USD
    "gas_limit": 250000,  # Gas limit for DEX transactions
    "max_trade_limit": 500,  # ✅ Add this line to fix the KeyError
    "stop_loss_threshold": 2.0,  # Stop-loss if price drops by 2%
    "trade_cooldown": 60  # Cooldown in seconds before retrying the same trade
}


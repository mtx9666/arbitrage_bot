# Cross-Exchange Arbitrage Scanner

Educational Python bot that **scans price spreads** across CEX (Binance, KuCoin) and DEX (Uniswap, PancakeSwap) venues, logs opportunities, and demonstrates automated execution patterns.

> **Disclaimer:** For research and learning only. Live trading involves financial risk, gas fees, slippage, and exchange ToS constraints. Not financial advice.

**Author:** Ali ([@mtx9666](https://github.com/mtx9666))

## What it does

1. Polls ETH/USDT (extensible to more pairs) on multiple exchanges
2. Computes cross-venue spread and profit % after threshold filter
3. Logs opportunities with structured trade journal
4. Executes simulated / configurable arbitrage routes via `TradeExecutor`

## Architecture

```
main.py          → orchestration loop
scanner.py       → ArbitrageScanner (CEX + DEX price feeds)
executor.py      → TradeExecutor (route execution)
config.py        → thresholds, API keys, pair registry
logger.py        → structured opportunity logging
exchanges/
  cex.py         → Binance / KuCoin REST wrappers
  dex.py         → Uniswap / PancakeSwap on-chain quotes
```

## Features

- Multi-venue price aggregation (CEX + DEX)
- Configurable minimum profit threshold
- Continuous scan loop with error recovery
- Trade logging for backtesting analysis
- Modular exchange adapters

## Setup

```bash
git clone https://github.com/mtx9666/arbitrage_bot.git
cd arbitrage_bot
pip install -r requirements.txt
```

Configure API keys in `config.py` (never commit secrets).

```bash
python main.py
```

## Configuration

Edit `config.py`:

```python
TRADE_SETTINGS = {
    "min_profit_threshold": 0.5,  # percent
    "scan_interval_sec": 5,
}
```

## What this demonstrates

- Real-time market data ingestion from multiple APIs
- Cross-exchange analytics & opportunity detection
- Event-driven trading bot architecture
- Python OOP with separation of scan / execute / log concerns

## Tech stack

Python · REST APIs · Web3 DEX quotes · asyncio-ready design

## License

MIT

import logging
from datetime import datetime

# Configure logging
LOG_FILE = f"logs/arbitrage_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_trade(route, buy_price, sell_price, profit_percent):
    """Logs successful arbitrage trades"""
    message = (
        f"💰 Arbitrage Trade Executed: {route}\n"
        f"💲 Buy at: {buy_price:.2f}, Sell at: {sell_price:.2f}\n"
        f"📈 Profit: {profit_percent:.2f}%\n"
        f"--------------------------"
    )
    logging.info(message)
    print(message)

def log_error(error_message):
    """Logs errors"""
    logging.error(error_message)
    print(f"❌ Error: {error_message}")

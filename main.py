import time
from scanner import ArbitrageScanner
from executor import TradeExecutor
from logger import log_trade, log_error  # Import logging functions

class ArbitrageBot:
    def __init__(self):
        self.scanner = ArbitrageScanner()
        self.executor = TradeExecutor()

    def run(self):
        """Runs the arbitrage bot continuously"""
        print("🚀 Starting Arbitrage Bot...")
        while True:
            try:
                print("🔍 Scanning for arbitrage opportunities...")
                for pair, data in self.scanner.token_pairs.items():
                    binance_price = self.scanner.binance.get_price(pair)
                    kucoin_price = self.scanner.kucoin.get_price(pair)
                    dex_price = self.scanner.uniswap.get_price(
                        data["dex"]["token_address"], data["dex"]["pair_contract"]
                    )

                    # Possible arbitrage paths
                    opportunities = [
                        ("Binance -> DEX", self.scanner.binance, self.scanner.uniswap, binance_price, dex_price),
                        ("KuCoin -> DEX", self.scanner.kucoin, self.scanner.uniswap, kucoin_price, dex_price),
                        ("DEX -> Binance", self.scanner.uniswap, self.scanner.binance, dex_price, binance_price),
                        ("DEX -> KuCoin", self.scanner.uniswap, self.scanner.kucoin, dex_price, kucoin_price)
                    ]

                    for route, buy_exchange, sell_exchange, buy_price, sell_price in opportunities:
                        profit_percent = ((sell_price - buy_price) / buy_price) * 100

                        if profit_percent >= self.scanner.profit_threshold:
                            print(f"💰 Arbitrage Found! {route}")
                            print(f"💲 Buy at {buy_price:.2f}, Sell at {sell_price:.2f}")
                            print(f"📈 Profit: {profit_percent:.2f}%")

                            # Log opportunity
                            log_trade(route, buy_price, sell_price, profit_percent)

                            # Execute trade
                            self.executor.execute_arbitrage(
                                buy_exchange=buy_exchange,
                                sell_exchange=sell_exchange,
                                symbol=pair,
                                token_address=data["dex"]["token_address"],
                                pair_contract=data["dex"]["pair_contract"],
                                buy_price=buy_price,
                                sell_price=sell_price
                            )

            except Exception as e:
                log_error(f"Error in bot loop: {e}")

            time.sleep(5)  # Scan every 5 seconds

if __name__ == "__main__":
    bot = ArbitrageBot()
    bot.run()

import time
from exchanges.cex import CEX
from exchanges.dex import DEX
from config import TRADE_SETTINGS

class ArbitrageScanner:
    def __init__(self):
        """Initialize CEX & DEX connections"""
        self.binance = CEX("binance")
        self.kucoin = CEX("kucoin")
        self.uniswap = DEX("ethereum")  # Uniswap (ETH chain)
        self.pancakeswap = DEX("bsc")   # PancakeSwap (BSC chain)
        self.token_pairs = {
            "ETH/USDT": {
                "dex": {
                    "token_address": "0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH Address
                    "pair_contract": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"   # Uniswap V2 WETH/USDT Pair
                }
            }
        }
        self.profit_threshold = TRADE_SETTINGS["min_profit_threshold"]

    def scan_arbitrage(self):
        """Scans for arbitrage opportunities"""
        print("🔍 Scanning for arbitrage opportunities...")

        for pair, data in self.token_pairs.items():
            try:
                # Fetch prices
                binance_price = self.binance.get_price(pair)
                kucoin_price = self.kucoin.get_price(pair)
                dex_price = self.uniswap.get_price(
                    data["dex"]["token_address"], data["dex"]["pair_contract"]
                )

                # Check for arbitrage opportunities
                opportunities = []
                opportunities.append(("Binance -> DEX", binance_price, dex_price))
                opportunities.append(("KuCoin -> DEX", kucoin_price, dex_price))
                opportunities.append(("DEX -> Binance", dex_price, binance_price))
                opportunities.append(("DEX -> KuCoin", dex_price, kucoin_price))

                for route, buy_price, sell_price in opportunities:
                    profit_percent = ((sell_price - buy_price) / buy_price) * 100

                    if profit_percent >= self.profit_threshold:
                        print(f"💰 Arbitrage Opportunity Found!")
                        print(f"🔄 {route}: Buy at {buy_price:.2f}, Sell at {sell_price:.2f}")
                        print(f"📈 Profit Potential: {profit_percent:.2f}%")
                        # Log the opportunity

            except Exception as e:
                print(f"❌ Error scanning {pair}: {e}")

if __name__ == "__main__":
    scanner = ArbitrageScanner()
    while True:
        scanner.scan_arbitrage()
        time.sleep(5)  # Scan every 5 seconds

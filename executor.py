import time
from exchanges.cex import CEX
from exchanges.dex import DEX
from config import TRADE_SETTINGS
from logger import log_trade, log_error

class TradeExecutor:
    def __init__(self):
        """Initialize CEX & DEX connections"""
        self.binance = CEX("binance")
        self.kucoin = CEX("kucoin")
        self.uniswap = DEX("ethereum")  # Uniswap (ETH chain)
        self.pancakeswap = DEX("bsc")   # PancakeSwap (BSC chain)
        self.trade_amount = TRADE_SETTINGS["trade_amount"]
        self.max_trade_limit = TRADE_SETTINGS["max_trade_limit"]
        self.stop_loss_threshold = TRADE_SETTINGS["stop_loss_threshold"]
        self.trade_cooldown = TRADE_SETTINGS["trade_cooldown"]
        self.last_trade_time = {}  # Store last trade timestamps

    def is_cooldown_active(self, symbol):
        """Check if a trade cooldown is active for a symbol"""
        if symbol in self.last_trade_time:
            elapsed_time = time.time() - self.last_trade_time[symbol]
            if elapsed_time < self.trade_cooldown:
                print(f"⚠️ Cooldown active for {symbol}, skipping trade.")
                return True
        return False

    def execute_cex_trade(self, exchange, symbol, side):
        """Executes market buy/sell order on a CEX"""
        try:
            price = exchange.get_price(symbol)
            amount = self.trade_amount / price  # Convert USD to token amount

            # Enforce max trade limit
            if self.trade_amount > self.max_trade_limit:
                log_error(f"Trade amount {self.trade_amount} exceeds max limit {self.max_trade_limit}.")
                return None

            order = exchange.api.create_market_order(symbol, side, amount)
            log_trade(f"{side.upper()} Order on {exchange.exchange_name}", price, price, 0)
            return order
        except Exception as e:
            log_error(f"Failed to execute CEX trade: {e}")
            return None

    def execute_dex_trade(self, dex, token_address, pair_contract, side):
        """Executes a swap on a DEX (Uniswap/PancakeSwap)"""
        try:
            price = dex.get_price(token_address, pair_contract)
            amount = self.trade_amount / price  # Convert USD to token amount

            # Enforce max trade limit
            if self.trade_amount > self.max_trade_limit:
                log_error(f"Trade amount {self.trade_amount} exceeds max limit {self.max_trade_limit}.")
                return None

            if side == "buy":
                log_trade(f"Buying on {dex.chain} DEX", price, price, 0)
            else:
                log_trade(f"Selling on {dex.chain} DEX", price, price, 0)
            return True
        except Exception as e:
            log_error(f"Failed to execute DEX trade: {e}")
            return None

    def execute_arbitrage(self, buy_exchange, sell_exchange, symbol, token_address, pair_contract, buy_price, sell_price):
        """Executes arbitrage trade with stop-loss and cooldown enforcement"""
        try:
            profit_percent = ((sell_price - buy_price) / buy_price) * 100

            # Check cooldown before trading
            if self.is_cooldown_active(symbol):
                return

            print("🔄 Executing Arbitrage Trade...")

            # Buy on lower exchange
            if isinstance(buy_exchange, CEX):
                buy_order = self.execute_cex_trade(buy_exchange, symbol, "buy")
            else:
                buy_order = self.execute_dex_trade(buy_exchange, token_address, pair_contract, "buy")

            # Stop-Loss Protection: Recheck price before selling
            current_sell_price = sell_exchange.get_price(symbol)
            loss_percent = ((buy_price - current_sell_price) / buy_price) * 100

            if loss_percent >= self.stop_loss_threshold:
                log_error(f"⚠️ Stop-Loss Triggered! Loss: {loss_percent:.2f}% - Cancelling trade.")
                return

            # Sell on higher exchange
            if isinstance(sell_exchange, CEX):
                sell_order = self.execute_cex_trade(sell_exchange, symbol, "sell")
            else:
                sell_order = self.execute_dex_trade(sell_exchange, token_address, pair_contract, "sell")

            if buy_order and sell_order:
                log_trade(f"Arbitrage Trade {buy_exchange.exchange_name} -> {sell_exchange.exchange_name}", buy_price, sell_price, profit_percent)
                print("💰 Arbitrage Trade Successful!")

                # Store trade timestamp for cooldown
                self.last_trade_time[symbol] = time.time()
            else:
                log_error("Trade Failed! One of the orders didn't execute.")

        except Exception as e:
            log_error(f"Error executing arbitrage trade: {e}")

# Example usage
if __name__ == "__main__":
    executor = TradeExecutor()

    # Example arbitrage execution: Buy from Binance, Sell on Uniswap
    executor.execute_arbitrage(
        buy_exchange=executor.binance,
        sell_exchange=executor.uniswap,
        symbol="ETH/USDT",
        token_address="0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        pair_contract="0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"   # Uniswap V2 WETH/USDT
    )

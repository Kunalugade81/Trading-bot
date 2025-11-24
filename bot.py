from binance.client import Client
from binance.enums import *
import logging
from config import API_KEY, API_SECRET, TESTNET_URL

logging.basicConfig(filename="logs/bot.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class BasicBot:
    def __init__(self):
        try:
            self.client = Client(API_KEY, API_SECRET, testnet=True)
            self.client.FUTURES_URL = TESTNET_URL
            logging.info("Bot initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing client: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            logging.info(f"Placing order: {side} {symbol} {order_type}")
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order response: {order}")
            return order

        except Exception as e:
            logging.error(f"Order failed: {e}")
            print(f" Error placing order: {e}")
            
    def stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        return self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=stop_price,
            price=limit_price,
            timeInForce="GTC"
        )

def main():
    bot = BasicBot()

    print("\n Binance Futures Testnet Trading Bot\n")

    symbol = input("Enter trading pair (ex: BTCUSDT): ").upper()
    side = input("Enter order side (BUY/SELL): ").upper()
    order_type = input("Order type (market/limit): ").lower()

    if order_type == "market":
        order_type = ORDER_TYPE_MARKET
        price = None
    elif order_type == "limit":
        order_type = ORDER_TYPE_LIMIT
        price = float(input("Enter limit price: "))
    else:
        print("Invalid order type")
        return

    quantity = float(input("Enter quantity: "))

    result = bot.place_order(symbol, side, order_type, quantity, price if price else None)

    print("\n Order Summary:")
    print(result)

if __name__ == "__main__":
    main()

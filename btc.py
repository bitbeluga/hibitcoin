import requests
import time
import asciichartpy

symbols = {
    "BTC-USDT": [],
    "ETH-USDT": [],
    "SOL-USDT": [],
    "SUI-USDT": [],
    "GPS-USDT": [],
    "M-USDT": []
}

def get_price(symbol):
    url = "https://www.okx.com/api/v5/market/ticker"
    try:
        resp = requests.get(url, params={"instId": symbol})
        resp.raise_for_status()
        return float(resp.json()["data"][0]["last"])
    except Exception as e:
        print(f"{symbol} 获取失败: {e}")
        return None

while True:
    for symbol in symbols:
        price = get_price(symbol)
        if price is not None:
            symbols[symbol].append(price)
            if len(symbols[symbol]) > 50:
                symbols[symbol].pop(0)

    print("\033c", end="")  # 清屏
    for symbol, history in symbols.items():
        print(f"{symbol} Price History (USDT, last 50 points):")
        if history:
            print(asciichartpy.plot(history, {'height': 10}))
            print(f"Latest: {history[-1]} USDT\n")
        else:
            print("暂无数据\n")

    time.sleep(10)

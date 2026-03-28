from hyperliquid.info import Info
from hyperliquid.utils import constants


def main():
    # Create Info instance for public market data only (no wallet needed)
    info = Info(constants.MAINNET_API_URL, skip_ws=False)

    # Subscribe to public market data only (no authentication required)
    info.subscribe({"type": "allMids"}, print)
    info.subscribe({"type": "l2Book", "coin": "BTC"}, print)
    info.subscribe({"type": "trades", "coin": "BTC"}, print)
    info.subscribe({"type": "candle", "coin": "BTC", "interval": "1m"}, print)
    info.subscribe({"type": "bbo", "coin": "BTC"}, print)
    info.subscribe({"type": "activeAssetCtx", "coin": "BTC"}, print)  # Perp
    info.subscribe({"type": "activeAssetCtx", "coin": "@1"}, print)  # Spot

    # Commented out user-specific subscriptions (require wallet authentication):
    # info.subscribe({"type": "userEvents", "user": address}, print)
    # info.subscribe({"type": "userFills", "user": address}, print)
    # info.subscribe({"type": "orderUpdates", "user": address}, print)
    # info.subscribe({"type": "userFundings", "user": address}, print)
    # info.subscribe({"type": "userNonFundingLedgerUpdates", "user": address}, print)
    # info.subscribe({"type": "webData2", "user": address}, print)
    # info.subscribe({"type": "activeAssetData", "user": address, "coin": "BTC"}, print)  # Perp only


if __name__ == "__main__":
    main()

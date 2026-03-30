import json
import time
from datetime import datetime, timedelta

from hyperliquid.info import Info
from hyperliquid.utils import constants

def get_last_week_btc_1m_data():
    """Get the x day's worth of 1-minute BTC candlestick data"""

    # Configuration
    output_directory = "/home/uboss/sc/hyperliquid-python-sdk/examples/data"  # Set your absolute path here
    days_back = 3  # Change this number to get data from N days ago

    # Initialize the Info client
    info = Info(constants.MAINNET_API_URL, skip_ws=True)

    # Calculate timestamps
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_back)

    # Convert to milliseconds (Unix timestamp * 1000)
    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)

    print(f"Fetching BTC 1-minute data from {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Start timestamp: {start_timestamp}")
    print(f"End timestamp: {end_timestamp}")

    try:
        # Get the candlestick data
        candles = info.candles_snapshot(
            name="BTC",
            interval="1m",
            startTime=start_timestamp,
            endTime=end_timestamp
        )

        print(f"\nRetrieved {len(candles)} candles")

        if candles:
            print("\nFirst candle:")
            print(json.dumps(candles[0], indent=2))

            print(f"\nLast candle:")
            print(json.dumps(candles[-1], indent=2))

            # Save to file
            filename = f"{output_directory}/btc_1m_data_{start_time.strftime('%Y%m%d')}_to_{end_time.strftime('%Y%m%d')}.json"
            with open(filename, 'w') as f:
                json.dump(candles, f, indent=2)

            print(f"\nData saved to {filename}")

            # Print some statistics
            print("\nData statistics:")
            print(f"Total candles: {len(candles)}")

            # Calculate expected candles based on time difference
            time_diff_days = (end_time - start_time).total_seconds() / (24 * 60 * 60)
            expected_candles = int(time_diff_days * 24 * 60)
            print(f"Expected candles ({time_diff_days:.1f} days * 24 hours * 60 minutes): {expected_candles}")

            if len(candles) > 0:
                # Calculate actual time range from data
                first_timestamp = candles[0]['t'] / 1000  # Convert back to seconds
                last_timestamp = candles[-1]['t'] / 1000

                first_datetime = datetime.fromtimestamp(first_timestamp)
                last_datetime = datetime.fromtimestamp(last_timestamp)

                print(f"Actual data range: {first_datetime} to {last_datetime}")

        else:
            print("No candle data received")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_last_week_btc_1m_data()
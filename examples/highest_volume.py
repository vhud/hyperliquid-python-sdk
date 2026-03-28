import json

from hyperliquid.info import Info
from hyperliquid.utils import constants

def find_top_volume_pairs():
    info = Info(constants.MAINNET_API_URL, skip_ws=True)  # skip_ws=True for REST-only

    # Get spot metadata to create name mapping
    spot_meta = info.spot_meta()
    spot_index_to_name = {}

    # Create token index to name mapping
    token_index_to_name = {}
    for token in spot_meta["tokens"]:
        token_index_to_name[token["index"]] = token["name"]

    # Create readable spot pair names from token combinations
    for spot_info in spot_meta["universe"]:
        if spot_info["tokens"]:  # Some entries might not have tokens
            base_idx, quote_idx = spot_info["tokens"]
            base_name = token_index_to_name.get(base_idx, f"TOKEN_{base_idx}")
            quote_name = token_index_to_name.get(quote_idx, f"TOKEN_{quote_idx}")
            readable_name = f"{base_name}/{quote_name}"
            spot_index_to_name[spot_info["index"]] = readable_name
        else:
            # Fallback to the name in meta if tokens not available
            spot_index_to_name[spot_info["index"]] = spot_info["name"]

    # Debug logging
    with open('debug_log.txt', 'w') as f:
        f.write("=== TOKEN INDEX TO NAME MAPPING ===\n")
        f.write(json.dumps(token_index_to_name, indent=2))
        f.write("\n\n=== SPOT INDEX TO READABLE NAME MAPPING ===\n")
        f.write(json.dumps(spot_index_to_name, indent=2))

    # Get perpetual data
    perp_meta, perp_ctxs = info.meta_and_asset_ctxs()

    # Get spot data
    spot_meta_data, spot_ctxs = info.spot_meta_and_asset_ctxs()

    # More debug logging
    with open('debug_log.txt', 'a') as f:
        f.write("\n\n=== RAW SPOT CTXS (first 3) ===\n")
        f.write(json.dumps(spot_ctxs[:3], indent=2))
        f.write("\n\n=== SPOT PAIR MAPPING PROCESS ===\n")

    # Collect all perp pairs with volumes
    perp_pairs = []
    for i, ctx in enumerate(perp_ctxs):
        volume = float(ctx.get('dayNtlVlm', '0'))
        pair_name = perp_meta['universe'][i]['name']
        perp_pairs.append((pair_name, volume, 'perp'))

    # Collect all spot pairs with volumes
    spot_pairs = []
    with open('debug_log.txt', 'a') as f:
        for i, ctx in enumerate(spot_ctxs[:10]):  # Log first 10 for debugging
            volume = float(ctx.get('dayNtlVlm', '0'))
            coin_index = ctx.get('coin', '')
            f.write(f"Entry {i}: coin_index='{coin_index}', volume={volume}\n")

            # Map @107 style indices to readable names
            if coin_index.startswith('@'):
                index = int(coin_index[1:])
                pair_name = spot_index_to_name.get(index, coin_index)  # fallback to index if not found
                f.write(f"  -> Parsed index {index}, mapped to '{pair_name}'\n")
            else:
                pair_name = coin_index
                f.write(f"  -> No @ prefix, using '{pair_name}'\n")

            spot_pairs.append((pair_name, volume, 'spot'))
            f.write(f"  -> Final: {pair_name}\n\n")

    # Sort both lists by volume (descending)
    perp_pairs.sort(key=lambda x: x[1], reverse=True)
    spot_pairs.sort(key=lambda x: x[1], reverse=True)

    # Combine all pairs for overall ranking
    all_pairs = perp_pairs + spot_pairs
    all_pairs.sort(key=lambda x: x[1], reverse=True)

    print("=== TOP 5 PERPETUAL PAIRS ===")
    for i, (pair, volume, market_type) in enumerate(perp_pairs[:5], 1):
        print(f"{i}. {pair}: ${volume:,.0f}")

    print("\n=== TOP 5 SPOT PAIRS ===")
    for i, (pair, volume, market_type) in enumerate(spot_pairs[:5], 1):
        print(f"{i}. {pair}: ${volume:,.0f}")

    print("\n=== TOP 5 OVERALL PAIRS ===")
    for i, (pair, volume, market_type) in enumerate(all_pairs[:5], 1):
        print(f"{i}. {pair} ({market_type}): ${volume:,.0f}")

if __name__ == "__main__":
    find_top_volume_pairs()

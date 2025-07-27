import os
from flask import Flask, request, jsonify, render_template
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime
import threading

# Load env variables
load_dotenv()
app = Flask(__name__)

# Tenderly RPC for Base chain
TENDERLY_RPC = os.getenv(
    "BASE_RPC") or "https://base.gateway.tenderly.co/1cAI6rLkKToMdpKceTtTAe"
w3 = Web3(Web3.HTTPProvider(TENDERLY_RPC))

# Your ERC-20 or ETH receiver address
RECEIVER = Web3.to_checksum_address(
    "0xeb5b687eb21dd4c7ae9d43b7d641f0d9e79d520d")

# ERC-20 contract (if tracking tokens)
ERC20_CONTRACT = os.getenv("ERC20_CONTRACT")  # optional
ERC20_ABI = []  # paste your ERC20 ABI here if needed

# In-memory ledger (or connect SQLite/Supabase for production)
ledger = []


@app.route('/')
def index():
    return render_template("dashboard.html", ledger=ledger)


@app.route('/claim', methods=['POST'])
def claim():
    data = request.json
    address = data.get("address")

    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    matched = [
        tx for tx in ledger if tx['from'] == Web3.to_checksum_address(address)
    ]

    if not matched:
        return jsonify({"error": "No deposit record found"}), 404

    # Simulated reward logic
    reward = sum([float(tx["value"]) for tx in matched])
    return jsonify({
        "message": "Eligible for reward",
        "wallet": address,
        "total_deposit_eth": reward,
        "status": "claimable"
    })


def monitor_deposits():
    print("🔍 Starting deposit monitor...")
    block = w3.eth.block_number

    while True:
        try:
            latest = w3.eth.block_number
            for b in range(block, latest + 1):
                block_data = w3.eth.get_block(b, full_transactions=True)
                for tx in block_data.transactions:
                    if tx.to and tx.to.lower() == RECEIVER.lower():
                        tx_hash = tx.hash.hex()
                        from_addr = tx['from']
                        value = w3.from_wei(tx.value, 'ether')

                        record = {
                            "hash": tx_hash,
                            "from": from_addr,
                            "value": float(value),
                            "timestamp": datetime.now().isoformat()
                        }
                        if tx_hash not in [t["hash"] for t in ledger]:
                            ledger.append(record)
                            print(f"💸 Received {value} ETH from {from_addr}")
            block = latest + 1
        except Exception as e:
            print(f"[ERROR] Monitor error: {e}")
        w3.middleware_onion.clear()


# Run in background thread
threading.Thread(target=monitor_deposits, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

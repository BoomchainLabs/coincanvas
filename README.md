# Coincanvas

On-chain deposit tracker with claimable token logic on the Base chain. This application is built using Flask and Web3 to monitor Ethereum deposits in real-time.

## Overview

Coincanvas continuously monitors a specified Ethereum address for incoming deposits and provides users with the ability to claim rewards based on their deposit history.

## Features

- Monitors Ethereum deposits in real-time.
- Allows users to claim rewards based on their deposit amount.
- Web-based dashboard to view deposit history.

## Requirements

- Python 3.11 or higher
- Flask
- Web3.py
- dotenv (for environment variable support)

## Installation

To get started, clone the repository and install the dependencies:

```bash
git clone https://github.com/BoomchainLabs/coincanvas.git
cd coincanvas
pip install -r requirements.txt

Configuration
Create a  file in the root directory and set the following environment variables:
BASE_RPC=https://base.gateway.tenderly.co/your_rpc_key
ERC20_CONTRACT=your_erc20_contract_address  # Optional

Running the Application
To start the application, run:

python3 main.py

The application will start and monitor deposits at the specified address.

You can access the dashboard at http://0.0.0.0:8080.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
BoomchainLabs support@boomchainlab.com


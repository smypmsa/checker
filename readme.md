# Pengu Airdrop Checker

Python script to check Solana wallet addresses for Pengu airdrop eligibility using Selenium browser automation.

## Overview

The script automates checking wallet addresses against the Pengu airdrop API using Chrome WebDriver. It processes addresses from a CSV file, handles rate limiting through delays, and saves results incrementally. If interrupted, it can resume from the last processed wallet.

## Prerequisites

- Python 3.8+
- Google Chrome browser
- Git

## Quick Setup

Clone and set up the project:
```bash
git clone https://github.com/yourusername/pengu-checker
cd pengu-checker
python -m venv venv

# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Create `wallets.csv` in the project root with one wallet address per line:
```text
4ebFWrxAhGSzMM2H6HUmrBuzNxRbLnu77mfgzvfp2Xi9
8j3hyCqNQJ3HDaS2lXg5FhGyBEwR8VtQHxHmLGYksxft
```

Optional: Add proxy configuration in `checker.py` if needed:
```python
proxy_list = [
    "proxy1:port1",
    "proxy2:port2"
]
```

## Usage

Run the script:
```bash
python checker.py
```

Results are saved to `results.csv` with columns: wallet_address, total, total_unclaimed. The script automatically skips previously processed wallets if `results.csv` exists.

## Development Notes

The script uses Selenium with anti-detection measures and random delays to avoid rate limiting. Key parameters like batch size and delays can be adjusted in the `process_wallets()` function.

## Troubleshooting

If you encounter WebDriver errors, ensure Chrome browser version matches the WebDriver version. For other issues, check that input CSV is properly formatted and you have stable internet connection.
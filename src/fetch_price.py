import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("FREECRYPTO_API_KEY")
base_url = "https://api.freecryptoapi.com/v1/getData"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def call_api_for_data(coin_name):
    response = requests.get(url=base_url, headers=headers, params={"symbol":coin_name})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error code: {response.status_code}")
        return None

def structure_data(data_from_api):
    asset_list = []

    for coin in data_from_api['symbols']:
        asset = coin.get("symbol")
        price = float(coin.get("last"))
        timestamp = coin.get("date")
        asset_list.append({'asset' : asset, 'price_usd' : price, 'timestamp' : timestamp })

    return asset_list

def main():
    if API_KEY is None:
        print("Error: API KEY is None !")
        return
    api_response = call_api_for_data("BTC + ETH + XRP")
    if api_response is None:
        print("Error: API response is None !")
        return
    asset_list = structure_data(api_response)
    print(json.dumps(asset_list, indent=2))

if __name__ == "__main__":
    main()
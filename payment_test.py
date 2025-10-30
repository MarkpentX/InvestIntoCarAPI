import requests
from datetime import datetime

hash = "a276f4f172a8fe7d5f58950c7a25a9d5e04f8e6a666f88d6d157dddee6dfa30a"
r = requests.get(f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}')
transaction_details = r.json()

timestamp = transaction_details.get("timestamp")  # миллисекунды
from_address = transaction_details["trc20TransferInfo"][0]["from_address"]
to_address = transaction_details["trc20TransferInfo"][0]["to_address"]
amount_raw = int(transaction_details["trc20TransferInfo"][0]["amount_str"])  # в минимальных единицах (6 знаков)
decimals = transaction_details["trc20TransferInfo"][0]["decimals"]

amount_usdt = amount_raw / (10 ** decimals)
amount_usd = amount_usdt

date_time = datetime.fromtimestamp(timestamp / 1000)

print(f"Дата и время транзакции: {date_time}")
print(f"Отправитель: {from_address}")
print(f"Получатель: {to_address}")
print(f"Сумма: {amount_usdt} USDT")

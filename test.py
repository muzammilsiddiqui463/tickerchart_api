import requests

r = requests.get("https://web-production-8a109.up.railway.app/data/")
print(r.json())
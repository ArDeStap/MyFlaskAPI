import requests

# api-endpoint
URL = "https://www.nalog.gov.ru/opendata/"

# PARAMS = {'name': 'ArDeStap', 'password': 'supperPassword', 'email':'MegaMail@example.u'}

# r = requests.post(url = URL, data = PARAMS)

r = requests.get(url=URL)

data = r.text

print(data)
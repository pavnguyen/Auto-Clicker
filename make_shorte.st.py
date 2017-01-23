import json

import requests

response = requests.put("https://api.shorte.st/v1/data/url", {"urlToShorten": "google.com"},
                        headers={"public-api-token": "465fba43219a1e95b506d85b2637db61"})
print(response.content)

decoded_response = json.loads(response.content)
print(decoded_response)
link_shorte_st = decoded_response['shortenedUrl']

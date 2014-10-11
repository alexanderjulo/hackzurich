from yummly import Client

TIMEOUT = 5.
RETRIES = 0
API_ID = '2bbb4000'
API_KEY = 'c154389b9e106d521c1c443349f2fbf7'


client = Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

search = client.search('green eggs and ham')
match = search.matches[0]

recipe = client.recipe(match.id)
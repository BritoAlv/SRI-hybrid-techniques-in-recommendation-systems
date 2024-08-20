import requests

TOTAL_PAGES = 2300
GUTENDEX_URL = 'https://gutendex.com/books/'

for i in range(563, TOTAL_PAGES + 1):
    url = f'{GUTENDEX_URL}?page={i}'
    response = requests.get(url)

    if response.status_code == 200:
        with open(f'./gutenberg_data/gutenberg_{i}.json', 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Invalid response code {response.status_code}")
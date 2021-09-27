import urllib.request,json
from .models import Quote


def get_quotes():
    get_quotes_url = 'http://quotes.stormconsultancy.co.uk/random.json'

    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)
        print(get_quotes_data)
    return get_quotes_response
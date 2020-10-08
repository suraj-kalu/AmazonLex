from django.shortcuts import render
import urllib3
import json
http = urllib3.PoolManager()

# Create your views here.
def index(request):
    response = http.request('GET', 'http://api.currencylayer.com/live?access_key=ACCESS_KEY')
    heros = json.loads(response.data.decode('utf-8'))
        # print(heros)
        # print(heros["quotes"])
     
    quotes = heros["quotes"]
    # print(quotes)
    new_format = list()
    for code, currency in quotes.items():
         new_format.append(code[3:] + " : " + str(currency) )
    return render(request, "currencyconverter/index.html", {
        
        "rates":new_format
    })
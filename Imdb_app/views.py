from django.shortcuts import render
import requests
from Imdb_app.forms import SearchForm

# Create your views here.
def home_page_view(request):
    context = {}

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data['search_selection'])
            # Api Call With the Search Results
            url = "https://imdb8.p.rapidapi.com/auto-complete"
            querystring = {"q": data['search_selection']}

            headers = {
                'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
                'x-rapidapi-host': "imdb8.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            
            reply = response.json()
            print(response.json())
    form = SearchForm()
    context.update({'form': form, 'reply': reply})
    return render(request, 'homepage.html', context)

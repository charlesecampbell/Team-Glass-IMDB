from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
import requests
from Imdb_app.forms import SearchForm, SignupForm, Comment_Form, LoginForm
from Imdb_app.models import ApplicationUser, Comment_model
from django.views import View
# Create your views here.


def home_page_view(request):
    context = {}
    reply = {}
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

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            reply = response.json()
            imageUrl = reply['d'][0]['i']['imageUrl']
            print(response.json())
    form = SearchForm()
    context.update({'form': form, 'reply': reply, 'imageUrl': imageUrl})
    return render(request, 'homepage.html', context)


class SignupView(View):
    form_class = SignupForm
    template_name = "signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "header": "Signup"})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = ApplicationUser.objects.create_user(
                username=data.get("username"),
                display_name=data.get("display_name"),
                password=data.get("password")
            )
            login(request, user)
            return redirect(reverse("home"))
        return render(request, self.template_name, {"form": form, "header": "Signup"})

# my guess is that we will be passing another parameter such as a movie id but for now this is how the details page will potentially look like
def details_view(request):
    print(request.user)
    # Here we will have all the information on the search
    # Along with the ability to post a comment for the specific movie
    context = {}
    # The object below will eventually be replaced with the actaul movie details
    movie = {
        'title': 'Test Movie',
        'description': '''Ipsum Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam condimentum, dolor ut facilisis hendrerit, augue nulla aliquam sapien, vel finibus velit nisi vel metus. Proin consectetur, eros at eleifend scelerisque, felis eros sagittis nisi, sed pellentesque felis odio sed nulla. Proin auctor, velit sed semper mollis, orci magna imperdiet magna, vel congue erat urna et ligula. 
        Donec iaculis mollis molestie. Phasellus et odio diam. Sed porta urna id sem sodales, eu iaculis neque tempus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Phasellus egestas ac felis sit amet finibus. Donec posuere, erat sit amet aliquet sollicitudin, felis enim consectetur nulla, in mollis mi nulla at ipsum. Quisque a dolor non turpis efficitur tempor ut 
        eget massa. Vivamus nec tincidunt metus. Aliquam feugiat molestie dui, sit amet convallis nibh convallis non. Nulla non vestibulum lacus. Morbi ac libero non lacus faucibus gravida id at nisl. In dapibus, mauris ac lacinia gravida, neque nibh imperdiet urna, a tincidunt nunc mauris sit amet libero. Pellentesque sapien lectus, suscipit quis risus sed, viverra tincidunt tellus'''
    }
    context.update({'movie':movie})
    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            new_item = Comment_model.objects.create(
                input_field= data['input_field'],
                movie= data['movie'],
                commenter= request.user,
                recommended= data['recommended'],
            )
    form = Comment_Form()
    context.update({'form': form})
    return render(request, 'details_page.html',context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                print('logged in')
                # above print will be replaced by redirect which will send user to homepage
    form = LoginForm()
    context.update({'form': form})
    return render(request, 'login.html', context)
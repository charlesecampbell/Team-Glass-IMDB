"""Imdb_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Imdb_app import views
from Imdb_project import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Imdb_app.views import SignupView, UserProfileView, add_to_likes
from Imdb_app.views import profile_update
from Imdb_app.views import SignupView, login_view, details_page
from Imdb_app.views import want_to_see, movies_have_seen

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/<int:applicationuser_id>/',
         UserProfileView.as_view(), name='user_profile'),
    path('update/<int:applicationuser_id>/', profile_update, name="update"),
    path('searchresults/', views.search_details_view, name='search_details'),
    path('details/<str:selection_id>/', details_page, name='details'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('actorspage/', views.ActorsView, name='actorspage'),
    path('addtolikes/<str:id>/', add_to_likes, name='add_to_likes'),
    path('addtoseen/<str:id>/', movies_have_seen, name='have_seen'),
    path('addtowantosee/<str:id>/', want_to_see, name='want_to_see'),
    path('admin/', admin.site.urls),
]

# added handler varables for views.py
handler404 = 'Imdb_app.views.error_404'
handler500 = 'Imdb_app.views.error_500'

# added to add images
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

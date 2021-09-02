from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .utils.pokemon_fetch import database_up_to_date, fetch_pokemon_count, update_database
from . import views
import sys

def on_startup():
    print("Starting initial data caching.")
    print("------------------------------")
    count = fetch_pokemon_count()
    if database_up_to_date(count):
        print("Database is up to date with External API.")

    else:
        print("Database needs updating. Proceeding...")
        print("-------------------------------------")
        update_database(api_count=count)
    

if 'runserver' in sys.argv:
    on_startup()

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pokemon_id>/', views.pokemon, name='Details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

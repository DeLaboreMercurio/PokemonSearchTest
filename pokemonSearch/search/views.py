import os

import requests
from django.conf import settings
from django.http import HttpResponse
from django.http.response import Http404
from django.template import loader

from .models import Pokemon
from .utils.pokemon_fetch import gather_detailed_information


def index(request):

    pokemons = Pokemon.objects.all()

    view_title = "Pokemon Finder - Gotta search'em all!"

    template = loader.get_template("search/index.html")
    context = {"pokemon_list": pokemons, "view_title": view_title}
    return HttpResponse(template.render(context, request))


def pokemon(request, pokemon_id):

    template = loader.get_template("search/detail.html")

    path = settings.MEDIA_URL

    context = {}
    try:
        pok = Pokemon.objects.get(id=pokemon_id)

        view_title = pok.name + " - Informacion detallada"

        detailed_information = gather_detailed_information(pok.url)

        image_path = ".." + path + pok.image.name

        context["pokemon_info"] = {"name": pok.name, "url": pok.url, "img": image_path}
        context["view_title"] = view_title
        context["detailed_information"] = detailed_information
    except Pokemon.DoesNotExist:

        raise Http404(
            "Pokemon does not exist."
        )  # A prettier custom 404 default page can be made. Probably by someone with better front-end skills.

    return HttpResponse(template.render(context, request))

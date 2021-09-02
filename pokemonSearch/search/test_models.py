from django.test import TestCase

from search.models import Pokemon


class ModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Pokemon.objects.create(name="Bulbasaur", url="https://pokeapi.co/api/v2/pokemon/1")
        Pokemon.objects.create(name="Ivysaur", url="https://pokeapi.co/api/v2/pokemon/2")

    def test_name_label(self):
        pokemon = Pokemon.objects.get(id=1)
        name_label = pokemon._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'name')

    def test_url_label(self):
        pokemon = Pokemon.objects.get(id=1)
        url_label = pokemon._meta.get_field('url').verbose_name
        self.assertEqual(url_label, 'url')

    def test_name_max_length(self):
        pokemon = Pokemon.objects.get(id=1)
        max_length = pokemon._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_url_max_length(self):
        pokemon = Pokemon.objects.get(id=1)
        max_length = pokemon._meta.get_field('url').max_length
        self.assertEqual(max_length, 500)

    def test_obj_name_is_pokemon_name(self):
        pokemon = Pokemon.objects.get(id=1)
        expected = "a"
        self.assertEqual(str(pokemon), pokemon.name)


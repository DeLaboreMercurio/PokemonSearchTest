from django.test import TestCase
from django.urls import reverse

from search.models import Pokemon


class IndexSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        Pokemon.objects.create(name="Pokemon 1", url="https://pokeapi.co/api/v2/pokemon/1")
        Pokemon.objects.create(name="Pokemon 2", url="https://pokeapi.co/api/v2/pokemon/2")
        Pokemon.objects.create(name="Pokemon 3", url="https://pokeapi.co/api/v2/pokemon/3")
        Pokemon.objects.create(name="Pokemon 4", url="https://pokeapi.co/api/v2/pokemon/4")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_unknown_pokemon_id_returns_404(self):
        response = self.client.get("/search/2000", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unknown_pokemon_id_returns_404(self):
        response = self.client.get("/search/2000", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/index.html")

    def test_all_four_pokemon_are_fetched(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("pokemon_list" in response.context)
        self.assertEqual(len(response.context["pokemon_list"]), 4)

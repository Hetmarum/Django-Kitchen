from django.test import TestCase
from kitchen.forms import CookCreationForm, DishForm, DishSearchForm, CookSearchForm, IngredientSearchForm
from kitchen.models import Cook, Dish, DishType, Ingredient
from decimal import Decimal


class CookCreationFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "username": "chef1",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 5,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.username, "chef1")
        self.assertEqual(cook.first_name, "John")
        self.assertEqual(cook.years_of_experience, 5)

    def test_form_missing_required_fields(self):
        form = CookCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient1 = Ingredient.objects.create(name="Salt")
        self.ingredient2 = Ingredient.objects.create(name="Pepper")
        self.cook = Cook.objects.create_user(username="chef", password="password123")

    def test_form_valid_data(self):
        form_data = {
            "name": "Dish1",
            "description": "Tasty dish",
            "price": "9.99",
            "dish_type": self.dish_type.id,
            "ingredients": [self.ingredient1.id, self.ingredient2.id],
            "cooks": [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_fields(self):
        form = DishForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("price", form.errors)
        self.assertIn("dish_type", form.errors)


class SearchFormsTest(TestCase):
    def test_dish_search_form_empty(self):
        form = DishSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "")

    def test_dish_search_form_with_data(self):
        form = DishSearchForm(data={"title": "Pizza"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Pizza")

    def test_cook_search_form_empty(self):
        form = CookSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "")

    def test_cook_search_form_with_data(self):
        form = CookSearchForm(data={"title": "chef1"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "chef1")

    def test_ingredient_search_form_empty(self):
        form = IngredientSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "")

    def test_ingredient_search_form_with_data(self):
        form = IngredientSearchForm(data={"title": "Salt"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Salt")

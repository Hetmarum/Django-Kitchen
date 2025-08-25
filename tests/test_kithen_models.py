from django.test import TestCase
from django.urls import reverse
from kitchen.models import Cook, Dish, DishType, Ingredient


class CookModelTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="chef1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            years_of_experience=5,
        )

    def test_str_method(self):
        self.assertEqual(str(self.cook), "chef1: John Doe")

    def test_get_absolute_url(self):
        url = self.cook.get_absolute_url()
        self.assertEqual(
            url, reverse("kitchen:cook-detail", args=[self.cook.id])
        )


class DishTypeModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_str_method(self):
        self.assertEqual(str(self.dish_type), "Main Course")


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato")

    def test_str_method(self):
        self.assertEqual(str(self.ingredient), "Tomato")


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.cook = Cook.objects.create_user(
            username="chef1",
            password="testpass"
        )
        self.ingredient = Ingredient.objects.create(name="Tomato")
        self.dish = Dish.objects.create(
            name="Pasta",
            description="Delicious pasta",
            price=9.99,
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.cook)
        self.dish.ingredients.add(self.ingredient)

    def test_str_method(self):
        self.assertEqual(
            str(self.dish), f"Pasta {self.dish_type} Price: {self.dish.price}"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.dish.get_absolute_url(),
            reverse("kitchen:dish-detail", args=[self.dish.id]),
        )

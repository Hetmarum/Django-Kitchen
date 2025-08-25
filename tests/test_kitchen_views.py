from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import Cook, Dish, DishType, Ingredient

User = get_user_model()



class DishListViewTest(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(username="chef1", password="testpass")
        self.client.login(username="chef1", password="testpass")

        self.dish_type = DishType.objects.create(name="Main Course")
        for i in range(10):
            Dish.objects.create(
                name=f"Dish{i}",
                description=f"Description {i}",
                price=i,
                dish_type=self.dish_type
            )

    def test_view_status_code(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_template_used(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_pagination(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertTrue("dish_list" in response.context)
        self.assertEqual(len(response.context["dish_list"]), 6)

    def test_search_functionality(self):
        response = self.client.get(reverse("kitchen:dish-list"), {"name": "Dish1"})
        dish_names = [dish.name for dish in response.context["dish_list"]]
        self.assertIn("Dish1", dish_names)

    def test_ordering_functionality(self):
        response = self.client.get(reverse("kitchen:dish-list"), {"order_by": "name_desc"})
        dish_names = [dish.name for dish in response.context["dish_list"]]
        self.assertEqual(dish_names[0], "Dish9")


class CookListViewTest(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(username="admin", password="testpass")
        self.client.login(username="admin", password="testpass")
        for i in range(10):
            Cook.objects.create_user(username=f"chef{i}", password="testpass")

    def test_search_username(self):
        response = self.client.get(reverse("kitchen:cook-list"), {"username": "chef1"})
        cooks = response.context["object_list"]
        cook_usernames = [cook.username for cook in cooks]

        self.assertIn("chef1", cook_usernames)

    def test_view_status_code(self):
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

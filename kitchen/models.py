from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", args=[str(self.id)])


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} {self.dish_type} Price: {self.price}"

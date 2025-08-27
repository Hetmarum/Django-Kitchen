from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from kitchen.utils import resize_image


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("username",)

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


class Ingredient(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def get_default_dish_type():
    return DishType.objects.get_or_create(name="None")[0].pk


class Dish(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(0.01)]
    )
    dish_type = models.ForeignKey(
        DishType, on_delete=models.SET_DEFAULT,
        default=get_default_dish_type,
        related_name="dishes",
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")
    picture = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} {self.dish_type} Price: {self.price}"

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.picture and not kwargs.get("raw", False):
            try:
                old = Dish.objects.get(pk=self.pk)
                picture_changed = old.picture != self.picture
            except Dish.DoesNotExist:
                picture_changed = True

            if picture_changed:
                resized = resize_image(
                    self.picture, size=(800, 800),
                    quality=85
                )
                self.picture.save(
                    self.picture.name, ContentFile(resized.read()), save=False
                )

        super().save(*args, **kwargs)

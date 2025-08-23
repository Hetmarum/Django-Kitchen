from django.urls import path


from kitchen.views import (
    IndexView,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishListView,
    DishCreateView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView,
    IngredientListView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
)


app_name = "kitchen"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
    path("dish_types/", DishTypeListView.as_view(), name="dish_type-list"),
    path("dish_types/create/", DishTypeCreateView.as_view(), name="dish_type-create"),
    path(
        "dish_types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish_type-update",
    ),
    path(
        "dish_types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish_type-delete",
    ),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/create", IngredientCreateView.as_view(), name="ingredient-create"),
    path("ingredients/<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient-update"),
    path("ingredients/<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient-delete"),
]

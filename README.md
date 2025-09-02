# django-kitchen
---
# site link
  * https://django-kitchen-3ab2.onrender.com/

# user to test features

  * user: user
  * password: user1234



# Kitchen Management System

A Django-based web application for managing cooks, dishes, dish types, and ingredients in a kitchen. Provides CRUD operations, search, filtering, and image handling.

## Features

* **User Management (Cooks)**

  * Custom `Cook` model extending Django’s `AbstractUser`.
  * Tracks years of experience.
  * Superusers and staff can create, update, and delete any cook.
  * Regular cooks can update their own profile (except permissions fields) and change their password.

* **Dish Types**

  * Categorize dishes with `DishType`.
  * CRUD operations available for superusers/staff.

* **Dishes**

  * Name, description, price, picture, and type.
  * Many-to-many relationships with `Cooks` and `Ingredients`.
  * Picture uploads are resized and optimized automatically.
  * Search and ordering by name, type, and price.

* **Ingredients**

  * Manage ingredients separately.
  * Searchable by name.

* **Security & Permissions**

  * Login required for all views.
  * Staff/superuser permissions enforced on sensitive actions.
  * Prevents editing/deleting superusers or self-deletion.

* **Forms & Utilities**

  * Custom creation and update forms for cooks and dishes.
  * `ConfirmDeleteMixin` for consistent delete confirmation.
  * `FormTemplateMixin` for consistent form rendering.
  * Image resizing utility for uploaded dish images.

* **Frontend Enhancements**

  * Select2 for better multi-select input UI on dishes.
  * Pagination for lists of cooks, dishes, ingredients, and dish types.

---

* Supports image resizing on save.
* Many-to-many relations with cooks and ingredients.
* Default dish type if none selected.

---

## Views

* **Index Dashboard**: Overview of cooks, dishes, and dish types.
* **Cook Views**: List, create, update, delete, and password change.
* **Dish Views**: List, create, update, delete, and detail.
* **DishType Views**: List, create, update, delete.
* **Ingredient Views**: List, create, update, delete.
* Search forms integrated for cooks, dishes, and ingredients.
* Pagination support in list views.

---

## Forms

* `CookCreationForm` – extends Django `UserCreationForm` with first name, last name, and experience.
* `DishForm` – full dish creation/update form.
* Search forms for `Cook`, `Dish`, and `Ingredient`.

---

## Utilities

* `resize_image` – Resizes uploaded dish images.
* `ConfirmDeleteMixin` – Adds confirmation template and previous URL context.
* `FormTemplateMixin` – Adds consistent context for forms with optional multipart support and extra JS scripts.

---

## URLs

* **Cooks**: `/cooks/` → list, `/cooks/create/`, `/cooks/<id>/update/`, etc.
* **Dish Types**: `/dish_types/` → list, `/dish_types/create/`, etc.
* **Dishes**: `/dishes/` → list, `/dishes/create/`, etc.
* **Ingredients**: `/ingredients/` → list, `/ingredients/create/`, etc.
* **Authentication**: `/login/`, `/logout/`.

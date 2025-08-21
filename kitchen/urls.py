from django.urls import path


from kitchen.views import IndexView


app_name = "kitchen"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

from django.urls import path

from restaurant.views import (
    index,
    CookerListView,
    CookerDetailView,
    DishListView,
    DishDetailView,
    DishTypeListView, CookerCreationView
)

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookerListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookerDetailView.as_view(), name="cook-detail"),
    path("cook/create/", CookerCreationView.as_view(), name="cook-create"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>", DishDetailView.as_view(), name="dish-detail"),
    path("types/", DishTypeListView.as_view(), name="type-list")
]

app_name = "restaurant"

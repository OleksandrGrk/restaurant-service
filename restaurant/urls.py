from django.urls import path

from restaurant.views import (
    index,
    CookerListView,
    CookerDetailView,
    DishListView,
    DishDetailView,
    DishTypeListView,
    CookerCreationView,
    DishCreateView,
    DishTypeCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookerListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookerDetailView.as_view(), name="cook-detail"),
    path("cook/create/", CookerCreationView.as_view(), name="cook-create"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish_type/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish/types/", DishTypeListView.as_view(), name="dish-type-list"),
]

app_name = "restaurant"

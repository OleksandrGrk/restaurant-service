from decimal import Decimal

from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from restaurant.models import Dish, DishType, Cooker

from restaurant.forms import (
    DishCreationForm, DishTypeCreationForm, CookerCreationForm, CookerSearchForm
)


COOKER_URL = reverse("restaurant:cook-list")
DISH_URL = reverse("restaurant:dish-list")


class TestForm(TestCase):
    def test_dish_is_valid(self):
        dish_type = DishType.objects.create(name="food")
        number_of_cooks = 2
        for cook_id in range(number_of_cooks):
            get_user_model().objects.create(
                first_name=f"test {cook_id}",
                last_name=f"surname {cook_id}",
                years_of_experience=cook_id + 1,
                username=f"username {cook_id}",
            )
        data = {
            "name": "test",
            "description": "some test text",
            "price": Decimal('10.5'),
            "dish_type": dish_type,
            "cooks": get_user_model().objects.all()
        }
        form = DishCreationForm(data=data)
        print(form.is_valid())
        print(form.errors)
        self.assertTrue(form.is_valid())
        # self.assertEquals(form.cleaned_data, data)

    def test_cooker_with_invalid_years_of_experience(self):
        data = {
            "username": "test",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "years_of_experience": 76,
        }

        form = CookerCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_cooker_search_form_label_field(self):
        form = CookerSearchForm()
        self.assertEquals(form.fields["username"].label, "")

    def test_cooker_search_form_required_field(self):
        form = CookerSearchForm()
        self.assertTrue(form.fields["username"].required)

    def test_cooker_search_form_max_length(self):
        form = CookerSearchForm()
        self.assertEquals(form.fields["username"].max_length, 255)

    def test_cooker_search_form_widget_placeholder_exist(self):
        form = CookerSearchForm()
        widget = form.fields["username"].widget
        self.assertTrue(
            widget.__dict__["attrs"]["placeholder"]
        )


class PublicCookerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(COOKER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateCookerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cooks = 10
        for cook_id in range(number_of_cooks):
            Cooker.objects.create(
                first_name=f"test {cook_id}",
                last_name=f"surname {cook_id}",
                username=f"username {cook_id}",
                years_of_experience=cook_id + 5
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_url_all_cooks_exist(self):
        response = self.client.get("/restaurant/cooks/")
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("restaurant:cook-list"))
        self.assertEquals(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse("restaurant:cook-list"))
        self.assertTemplateUsed(response, "restaurant/cook_list.html")

    def test_pagination_is_2(self):
        response = self.client.get(reverse("restaurant:cook-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEquals(len(response.context["cooker_list"]), 2)

    def test_page_6_with_one_cooker(self):
        response = self.client.get(reverse("restaurant:cook-list") + "?page=6")
        self.assertEquals(len(response.context["cooker_list"]), 1)

    def test_create_cooker(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "years_of_experience": 12,
        }

        self.client.post(reverse("restaurant:cook-create"), data=form_data)
        new_cooker = get_user_model().objects.get(username=form_data["username"])

        self.assertEquals(new_cooker.username, form_data["username"])
        # self.assertEquals(new_cooker.first_name, form_data["first_name"])
        self.assertEquals(
            new_cooker.years_of_experience,
            form_data["years_of_experience"]
        )


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_retrieve_dishes(self):
        dish_type = DishType.objects.create(
            name="test",
        )
        Dish.objects.create(name="Pizza", dish_type=dish_type, price=10.5)
        Dish.objects.create(name="Soup", dish_type=dish_type, price=11.5)
        response = self.client.get(DISH_URL)
        self.assertEquals(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEquals(list(response.context["car_list"]), list(dishes))
#
#
# class CarSearchModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         manufacturer = Manufacturer.objects.create(
#             name="test",
#             country="country1"
#         )
#         models = [
#             "nissan",
#             "opel",
#             "volskvagen",
#             "mercedes",
#             "kia",
#             "shevrolet",
#             "renault"
#         ]
#         for model in models:
#             Car.objects.create(model=model, manufacturer=manufacturer)
#
#     def setUp(self) -> None:
#         self.user = get_user_model().objects.create_user(
#             username="test_user", password="test1234"
#         )
#
#         self.client.force_login(self.user)
#
#     def test_search_model_car_with_single_letter(self):
#         char = "a"
#         response = self.client.get(f"/cars/?model={char}")
#         car_with_letter_a = Car.objects.filter(model__icontains=char)
#         self.assertEquals(
#             list(response.context["car_list"]),
#             list(car_with_letter_a)[:3]
#         )
#
#     def test_search_model_car_with_uppercase_letters(self):
#         char = "AN"
#         response = self.client.get(f"/cars/?model={char}")
#         car_with_letter_a = Car.objects.filter(model__icontains=char)
#         self.assertEquals(
#             list(response.context["car_list"]),
#             list(car_with_letter_a)[:3]
#         )
#
#     def test_search_model_car_page_2(self):
#         char = "A"
#         response = self.client.get(f"/cars/?model={char}&page=2")
#         car_with_letter_a = Car.objects.filter(model__icontains=char)
#         self.assertEquals(
#             list(response.context["car_list"]),
#             list(car_with_letter_a)[3:6]
#         )
#
#     def test_search_model_car_by_exact_name(self):
#         response = self.client.get("/cars/?model=opel")
#         opel = Car.objects.filter(model="opel")
#         self.assertEquals(list(response.context["car_list"]), list(opel))
#
#
# class ModelTests(TestCase):
#     def test_manufacturer_str(self):
#         manufacturer = Manufacturer.objects.create(
#             name="Opel",
#             country="Germany"
#         )
#         self.assertEquals(
#             str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
#         )
#
#     def test_driver_str(self):
#         driver = get_user_model().objects.create(
#             username="michael",
#             first_name="Michael",
#             last_name="Schumacher",
#             password="test1234",
#         )
#
#         self.assertEquals(
#             str(driver),
#             f"{driver.username} ({driver.first_name} {driver.last_name})"
#         )
#
#     def test_driver_with_license_number(self):
#         username = "michael"
#         first_name = "Michael"
#         last_name = "Schumacher"
#         password = "test1234"
#         license_number = "LICENSE"
#         driver = get_user_model().objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#             license_number=license_number,
#         )
#
#         self.assertEquals(driver.username, username)
#         self.assertEquals(driver.license_number, license_number)
#         self.assertTrue(driver.check_password(password))
#
#     def test_car_str(self):
#         manufacturer = Manufacturer.objects.create(
#             name="Opel",
#             country="Germany"
#         )
#         car = Car.objects.create(model="audi", manufacturer=manufacturer)
#
#         self.assertEquals(str(car), car.model)
#
#     def test_manufacturer_ordering(self):
#         manufacturer1 = Manufacturer.objects.create(
#             name="opel",
#             country="country1"
#         )
#         manufacturer2 = Manufacturer.objects.create(
#             name="alfa romeo", country="country2"
#         )
#         manufacturer3 = Manufacturer.objects.create(
#             name="nissan",
#             country="country3"
#         )
#         manufacturer4 = Manufacturer.objects.create(
#             name="citroen",
#             country="country4"
#         )
#
#         all_manufacturers = list(Manufacturer.objects.all())
#
#         self.assertEquals(
#             all_manufacturers,
#             [manufacturer2, manufacturer4, manufacturer3, manufacturer1],
#         )
#
#     def test_driver_absolute_url(self):
#         driver = get_user_model().objects.create(
#             username="michael",
#             first_name="Michael",
#             last_name="Schumacher",
#             password="test1234",
#         )
#         self.assertEquals(driver.get_absolute_url(), f"/drivers/{driver.id}/")
#
#     def test_driver_license_number_max_length(self):
#         driver = get_user_model().objects.create(
#             username="michael",
#             first_name="Michael",
#             last_name="Schumacher",
#             password="test1234",
#         )
#         self.assertEquals(
#             driver._meta.get_field("license_number").max_length, 255
#         )
#
#     def test_car_blank_false(self):
#         car = Car.objects.create(
#             model="Opel",
#             manufacturer=Manufacturer.objects.create(
#                 name="test",
#                 country="country1"
#             ),
#         )
#         self.assertFalse(car._meta.get_field("model").blank)
#
#
# class AdminSiteTests(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             username="test", password="test1234"
#         )
#
#         self.client.force_login(self.admin_user)
#         self.driver = get_user_model().objects.create_user(
#             username="testdriver",
#             password="test1234",
#             license_number="LICENSE"
#         )
#
#     def test_driver_license_listed(self):
#         url = reverse("admin:taxi_driver_changelist")
#         response = self.client.get(url)
#         self.assertContains(response, self.driver.license_number)
#
#     def test_driver_detail_license_listed(self):
#         url = reverse("admin:taxi_driver_change", args=[self.driver.id])
#         response = self.client.get(url)
#
#         self.assertContains(response, self.driver.license_number)

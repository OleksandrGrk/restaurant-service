from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from restaurant.models import Cooker, DishType, Dish


class CookerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cooker
        fields = UserCreationForm.Meta.fields + ("years_of_experience",)

    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]
        if years > 75:
            raise ValidationError("You can`t be so old!")
        return years


class DishCreationForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishTypeCreationForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"


class CookerSearchForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter cook name..."}
        )
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter dish name..."}
        )
    )

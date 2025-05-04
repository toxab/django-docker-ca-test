from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'unit_price']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']

class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['ingredient', 'quantity']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['menu_item']

class RecipeRequirementInlineForm(forms.Form):
    def __init__(self, *args, **kwargs):
        ingredients = kwargs.pop('ingredients')
        super().__init__(*args, **kwargs)
        for ingredient in ingredients:
            self.fields[f'ingredient_{ingredient.id}'] = forms.FloatField(
                label=f'{ingredient.name} ({ingredient.unit})',
                min_value=0,
                required=False
            )
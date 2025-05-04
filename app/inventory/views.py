from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm, RecipeRequirementInlineForm
from django.db import transaction
from django.contrib import messages
from django.views.generic import TemplateView
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return redirect('dashboard')

# Ingredient views
@login_required
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'inventory/ingredient_list.html', {'ingredients': ingredients})

@login_required
def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    ingredient.delete()
    return redirect('ingredient_list')

@login_required
def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()
    return render(request, 'inventory/ingredient_form.html', {'form': form})

@login_required
def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'inventory/ingredient_form.html', {'form': form})

@login_required
def ingredient_add(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()
    return render(request, 'inventory/ingredient_form.html', {'form': form})

@login_required
def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'inventory/ingredient_form.html', {'form': form, 'update': True})

# Purchase views
@login_required
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-timestamp')
    return render(request, 'inventory/purchase_list.html', {'purchases': purchases})

@login_required
def purchase_add(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            menu_item = form.cleaned_data['menu_item']
            requirements = RecipeRequirement.objects.filter(menu_item=menu_item)

            for req in requirements:
                if req.ingredient.quantity < req.quantity:
                    messages.error(request, f"Not enough {req.ingredient.name} in stock.")
                    return redirect('purchase_add')

            with transaction.atomic():
                for req in requirements:
                    req.ingredient.quantity -= req.quantity
                    req.ingredient.save()

                form.save()
                messages.success(request, f"Purchased {menu_item.title}")
                return redirect('purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'inventory/purchase_add.html', {'form': form})

# Menu views
@login_required
def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'inventory/menu_list.html', {'menu_items': menu_items})

@login_required
def menu_add(request):
    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        requirement_form = RecipeRequirementInlineForm(request.POST, ingredients=ingredients)

        if form.is_valid() and requirement_form.is_valid():
            menu_item = form.save()

            added_any = False
            for ingredient in ingredients:
                qty = requirement_form.cleaned_data.get(f'ingredient_{ingredient.id}')
                if qty and qty > 0:
                    RecipeRequirement.objects.create(
                        menu_item=menu_item,
                        ingredient=ingredient,
                        quantity=qty
                    )
                    added_any = True

            if not added_any:
                menu_item.delete()
                form.add_error(None, "You must add at least one ingredient.")
            else:
                return redirect('menu_list')
    else:
        form = MenuItemForm()
        requirement_form = RecipeRequirementInlineForm(ingredients=ingredients)

    return render(request, 'inventory/menu_add.html', {
        'form': form,
        'requirement_form': requirement_form,
    })

#  Recipe views
@login_required
def recipe_add(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    if request.method == 'POST':
        form = RecipeRequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.menu_item = menu_item
            requirement.save()
            messages.success(request, f"✅ Added ingredient to {menu_item.title}")
            return redirect('recipe_add', menu_item_id=menu_item.id)
    else:
        form = RecipeRequirementForm()
    return render(request, 'inventory/recipe_add.html', {'form': form, 'menu_item': menu_item})

@login_required
def add_requirements(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        for ingredient in ingredients:
            quantity = request.POST.get(f'ingredient_{ingredient.id}')
            if quantity:
                try:
                    quantity = float(quantity)
                    if quantity > 0:
                        RecipeRequirement.objects.create(
                            menu_item=menu_item,
                            ingredient=ingredient,
                            quantity=quantity
                        )
                except ValueError:
                    continue
        return redirect('menu_list')

    return render(request, 'inventory/add_requirements.html', {
        'menu_item': menu_item,
        'ingredients': ingredients,
    })

#  Report views
@login_required
def report(request):
    total_revenue = Purchase.objects.aggregate(
        revenue=Sum('menu_item__price')
    )['revenue'] or 0

    used_ingredients = RecipeRequirement.objects.annotate(
        total_cost=ExpressionWrapper(
            F('quantity') * F('ingredient__unit_price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    total_cost = sum(item.total_cost for item in used_ingredients)

    profit = total_revenue - total_cost

    return render(request, 'inventory/report.html', {
        'revenue': total_revenue,
        'cost': total_cost,
        'profit': profit,
    })

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = Purchase.objects.select_related('menu_item')
        total_revenue = sum(Decimal(str(p.menu_item.price)) for p in purchases)

        total_cost = Decimal('0')
        for purchase in purchases:
            for req in purchase.menu_item.reciperequirement_set.select_related('ingredient'):
                cost = Decimal(str(req.quantity)) * req.ingredient.unit_price
                total_cost += cost

        context.update({
            'inventory': Ingredient.objects.all(),
            'menu_items': MenuItem.objects.prefetch_related('reciperequirement_set__ingredient'),
            'purchases': purchases,
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'profit': total_revenue - total_cost,
        })
        return context
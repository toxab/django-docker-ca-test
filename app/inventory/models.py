from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()  # how much of the ingredient is required

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} {self.ingredient.name} for {self.menu_item.title}"

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.title} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=90)
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=220)
    price = models.PositiveIntegerField()
    is_vegetarian = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FoodOrder(models.Model):
    reference = models.CharField(max_length=12, unique=True)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=24, default="Received")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference

class FoodOrderLine(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=90)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.PositiveIntegerField()

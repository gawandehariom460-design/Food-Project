from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="MenuItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=90)),
            ("category", models.CharField(max_length=30)),
            ("description", models.CharField(max_length=220)),
            ("price", models.PositiveIntegerField()),
            ("is_vegetarian", models.BooleanField(default=True)),
            ("is_available", models.BooleanField(default=True)),
        ]),
        migrations.CreateModel(name="FoodOrder", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("reference", models.CharField(max_length=12, unique=True)),
            ("total", models.PositiveIntegerField()),
            ("status", models.CharField(default="Received", max_length=24)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name="FoodOrderLine", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("item_name", models.CharField(max_length=90)),
            ("quantity", models.PositiveSmallIntegerField()),
            ("unit_price", models.PositiveIntegerField()),
            ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="menu.foodorder")),
        ]),
    ]

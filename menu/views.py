from secrets import token_hex

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import FoodOrder, FoodOrderLine, MenuItem

SAMPLE_MENU = [
    ("Paneer Tikka Bowl", "Mains", "Grilled paneer, rice, greens and house chutney.", 260, True),
    ("Garden Veg Thali", "Mains", "Seasonal vegetables, dal, roti and rice.", 220, True),
    ("Crispy Corn", "Small plates", "Sweet corn tossed with lime and mild spices.", 150, True),
    ("Masala Fries", "Small plates", "Golden potato fries with a house spice blend.", 120, True),
    ("Mango Lassi", "Drinks", "Chilled yogurt drink with ripe mango.", 90, True),
    ("Chocolate Brownie", "Dessert", "Warm cocoa brownie for a sweet finish.", 110, True),
]

def seed_menu():
    if not MenuItem.objects.exists():
        MenuItem.objects.bulk_create([
            MenuItem(name=n, category=c, description=d, price=p, is_vegetarian=v)
            for n, c, d, p, v in SAMPLE_MENU
        ])

def build_cart(request):
    rows, total = [], 0
    for raw_id, qty in request.session.get("cart", {}).items():
        item = MenuItem.objects.filter(pk=raw_id, is_available=True).first()
        if item and int(qty) > 0:
            subtotal = item.price * int(qty)
            rows.append({"item": item, "quantity": int(qty), "subtotal": subtotal})
            total += subtotal
    return rows, total

@require_http_methods(["GET", "POST"])
def menu(request):
    seed_menu()
    if request.method == "POST":
        action = request.POST.get("action")
        cart = request.session.get("cart", {})
        if action == "add":
            item = MenuItem.objects.filter(pk=request.POST.get("item_id"), is_available=True).first()
            if item:
                key = str(item.pk)
                cart[key] = min(10, int(cart.get(key, 0)) + 1)
                request.session["cart"] = cart
                messages.success(request, f"{item.name} added to your order.")
            else:
                messages.error(request, "That menu item is unavailable.")
            return redirect("menu")
        if action == "update":
            for item in MenuItem.objects.filter(is_available=True):
                try:
                    qty = max(0, min(10, int(request.POST.get(f"qty_{item.pk}", "0"))))
                except ValueError:
                    qty = 0
                if qty:
                    cart[str(item.pk)] = qty
                else:
                    cart.pop(str(item.pk), None)
            request.session["cart"] = cart
            return redirect("/?view=cart")
        if action == "checkout":
            rows, total = build_cart(request)
            if not rows:
                messages.error(request, "Add an item before placing an order.")
                return redirect("menu")
            with transaction.atomic():
                order = FoodOrder.objects.create(reference=token_hex(4).upper(), total=total)
                FoodOrderLine.objects.bulk_create([
                    FoodOrderLine(order=order, item_name=row["item"].name, quantity=row["quantity"], unit_price=row["item"].price)
                    for row in rows
                ])
            request.session["cart"] = {}
            messages.success(request, f"Demo pickup order {order.reference} received. No payment was taken.")
            return redirect("menu")

    term = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    vegetarian = request.GET.get("veg") == "1"
    items = MenuItem.objects.filter(is_available=True)
    if term:
        items = items.filter(name__icontains=term) | items.filter(description__icontains=term)
    if category:
        items = items.filter(category=category)
    if vegetarian:
        items = items.filter(is_vegetarian=True)
    rows, total = build_cart(request)
    return render(request, "index.html", {
        "items": items.order_by("category", "name"),
        "categories": MenuItem.objects.values_list("category", flat=True).distinct(),
        "term": term, "category": category, "vegetarian": vegetarian,
        "cart": rows, "cart_total": total,
        "cart_count": sum(row["quantity"] for row in rows),
        "show_cart": request.GET.get("view") == "cart",
    })

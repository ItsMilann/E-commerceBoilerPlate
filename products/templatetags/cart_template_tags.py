from django import template
from products.models import Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            count = qs[0].product.count()
            if count != None:
                return count
            else:
                count= 0
            return count
    return 0
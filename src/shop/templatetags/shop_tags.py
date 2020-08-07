from django import template

from ..models import ProductCategory
from ..forms import AddToCartForm


register = template.Library()


@register.inclusion_tag('shop/_product_category_menu.html')
def product_category_menu():
    """Product category menu tag."""
    return {
        'category_list': ProductCategory.objects.all()
    }


@register.inclusion_tag('shop/_add_to_cart_form.html', takes_context=True)
def add_to_cart_form(context, product_id, quantity=1):
    """Tag for form to add product to cart."""
    return {
        'form': AddToCartForm(
            initial={
                'product_id': product_id,
                'quantity': quantity,
            }
        ),
        'next': context['request'].path,
    }


@register.simple_tag(takes_context=True)
def num_items_in_cart(context):
    """Tag for number of items in cart."""
    try:
        return sum(context['request'].session['cart'].values())
    except KeyError:
        return 0

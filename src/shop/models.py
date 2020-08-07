from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class ProductCategory(models.Model):
    """Model for product categories."""
    name = models.CharField(
        verbose_name=_('category name'),
        max_length=128,
    )

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class Product(models.Model):
    """Model for products."""
    # Or M2M here?
    category = models.ForeignKey(
        ProductCategory,
        verbose_name=_('category'),
        on_delete=models.PROTECT,
    )

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='products/',
        blank=True,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Order(models.Model):
    """Model for orders."""
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    products = models.ManyToManyField(
        Product,
        through='OrderItem',
        through_fields=('order', 'product'),
        related_name='orders',
        # related_query_name='application',
    )

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=150,
    )

    patronymic_name = models.CharField(
        verbose_name=_('patronymic name'),
        blank=True,
        max_length=150,
    )

    last_name = models.CharField(
        verbose_name=_('second name'),
        max_length=150,
    )

    address = models.TextField(
        verbose_name=_('address for delivery'),
    )

    phone = PhoneNumberField(
        verbose_name=_('phone number'),
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('e-mail address'),
        blank=True,
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def get_full_name(self):
        """Get full name of buyer."""
        if self.patronymic_name:
            return '{} {} {}'.format(
                self.first_name,
                self.patronymic_name,
                self.last_name,
            )

        return '{} {}'.format(
            self.first_name,
            self.last_name,
        )


class OrderItem(models.Model):
    """Models fo order items."""
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity')
    )

    class Meta:
        # No two order lines with same product.
        unique_together = [
            'order',
            'product',
        ]
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

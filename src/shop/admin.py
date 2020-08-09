from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_category_name',
        'image',
        'description',
        'price',
    )

    def get_category_name(self, obj):
        """Get name of product category."""
        return '{}'.format(
            obj.category.name,
        )

    get_category_name.short_description = _('product category')



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

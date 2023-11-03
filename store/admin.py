
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TaggedItem
from . import models
# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# SEARCH FOR DJANGO MODELADMIN->MODELADMIN OPTIONS


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    exclude = ['promotions']
    inlines = [TagInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 25
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
# admin.site.register(models.Product,ProductAdmin)

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} products were successfully updated'
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # return collection.products_count
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 25
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']

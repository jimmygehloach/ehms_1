from django.contrib import admin

from ehms.inventory.models import ItemCategory, Item, Supplier, ReceivedDetail, \
    IssuedDetail, Inventory


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


# @admin.register(IssueInventory)
# class IssueInventoryAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = [
#         'get_issued_detail',
#         'get_item',
#         'quantity',
#         'price',
#         'vat',
#         'discount',
#         'total_price',
#     ]
#     list_filter = ('status', 'created', 'issued_detail',)
#     ordering = ('-created',)
#     search_fields = ['pk', ]
#
#     def get_item(self, obj):
#         return obj.item.item_name
#
#     def get_issued_detail(self, obj):
#         return obj.issued_detail.bill_number


# @admin.register(ReceiveInventory)
# class ReceiveInventoryAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = [
#         'get_received_detail',
#         'get_item',
#         'quantity',
#         'price',
#         'vat',
#         'discount',
#         'total_price',
#     ]
#     list_filter = ('status', 'created', 'received_detail', )
#     ordering = ('-created', )
#     search_fields = ['pk', ]
#
#     def get_item(self, obj):
#         return obj.item.item_name
#
#     def get_received_detail(self, obj):
#         return obj.received_detail.bill_number


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'get_item',
        'get_issued_detail',
        'get_received_detail',
        'received_quantity',
        'issued_quantity',
        'price',
        'vat',
        'discount',
        'total_price',
    ]
    list_filter = ('status', 'created', 'issued_detail', 'received_detail', )
    ordering = ('-created',)
    search_fields = ['pk', ]

    def get_item(self, obj):
        return obj.item.item_name

    def get_issued_detail(self, obj):
        if obj.issued_detail:
            return obj.issued_detail.bill_number

    def get_received_detail(self, obj):
        if obj.received_detail:
            return obj.received_detail.bill_number


@admin.register(ReceivedDetail)
class ReceivedDetailAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'bill_number',
        'total_items',
        'gross_amount',
        'status',
        'created',
    ]
    list_filter = ('status', 'created', )
    ordering = ('-created', )
    search_fields = ['bill_number', ]


@admin.register(IssuedDetail)
class IssuedDetailAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'bill_number',
        'get_department',
        'total_items',
        'gross_amount',
        'status',
        'created',
    ]
    list_filter = ('status', 'created',)
    ordering = ('-created',)
    search_fields = ['bill_number', ]

    def get_department(self, obj):
        return obj.department.name





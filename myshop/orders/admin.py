from django.contrib import admin
from .models import Order, OrderItem
# for custom admin action
import csv
import datetime
from django.http import HttpResponse
# For custom admin view
from django.urls import reverse
from django.utils.safestring import mark_safe


# this is a custom admin action to export objects as csv
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name_plural)
    writer = csv.writer(response)

    # retrieves all fields of related model except many to many and one to many
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows now
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# For custom admin view
# For adding the option of showing product deatail in orders objectlist in admin
def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))

# For adding the option of pdf generate into the orders objectlist in admin
def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail, order_pdf]
    # in above list we can add 'braintree_id' field too
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
    # we can add the 'export_to_csv' admin action to any 'ModelAdmin' class so we will add that to this 'ModelAdmin' class named 'OrderAdmin'
    actions = [export_to_csv]
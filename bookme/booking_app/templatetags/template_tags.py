from django import template
register = template.Library()

@register.filter
def sort(queryset):
    return queryset.order_by('date', 'time_in')
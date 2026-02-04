from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def sort_url(context, field_name):
    """Return a query string that toggles sorting for field_name while preserving other GET params."""
    request = context.get('request')
    if not request:
        return ''
    params = request.GET.copy()
    current = params.get('sort', '')
    # toggle
    if current == field_name:
        new = f'-{field_name}'
    elif current == f'-{field_name}':
        new = field_name
    else:
        new = field_name
    params['sort'] = new
    params.pop('page', None)
    qs = params.urlencode()
    return f'?{qs}' if qs else ''

@register.simple_tag(takes_context=True)
def sort_indicator(context, field_name):
    request = context.get('request')
    if not request:
        return ''
    current = request.GET.get('sort','')
    # Provide arrow visible to sighted users and hidden descriptive text for screen readers
    if current == field_name:
        return format_html("<span class='ms-1' aria-hidden='true'>{}</span><span class='visually-hidden'>{}</span>", "↑", "Отсортировано по возрастанию")
    if current == f'-{field_name}':
        return format_html("<span class='ms-1' aria-hidden='true'>{}</span><span class='visually-hidden'>{}</span>", "↓", "Отсортировано по убыванию")
    return ''

@register.simple_tag(takes_context=True)
def url_with_page(context, page_num):
    request = context.get('request')
    if not request:
        return f'?page={page_num}'
    params = request.GET.copy()
    params['page'] = page_num
    qs = params.urlencode()
    return f'?{qs}' if qs else ''

@register.simple_tag(takes_context=True)
def aria_sort(context, field_name):
    """Return aria-sort value for accessibility: 'ascending', 'descending' or 'none'"""
    request = context.get('request')
    if not request:
        return 'none'
    current = request.GET.get('sort','')
    if current == field_name:
        return 'ascending'
    if current == f'-{field_name}':
        return 'descending'
    return 'none'

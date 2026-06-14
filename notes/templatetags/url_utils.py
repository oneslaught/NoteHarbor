from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    request = context['request']
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    return params.urlencode()
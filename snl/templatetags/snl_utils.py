from django import template

register = template.Library()

@register.filter
def getitem ( item, string ):
  return item.get(string,'')

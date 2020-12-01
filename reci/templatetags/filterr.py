from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter(name='selector')
def selector(a,b):
      if a in b:
        return "selected"
      else:
          pass
            
   


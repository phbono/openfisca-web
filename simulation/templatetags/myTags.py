from django import template

register = template.Library()

def show_field(field):
    label = field.name[1:].upper()
    return {'label': label, 'field': field, 'errors': field.errors}

def show_case(field):
    label = field.name[-1].upper()
    return {'label': label, 'field': field, 'errors': field.errors}


register.inclusion_tag('simulation/f0xxTemplate.html')(show_field)
register.inclusion_tag('simulation/f0xxTemplate.html')(show_case)

from django import template
import os

register = template.Library()

@register.filter
def extensao(nome_arquivo):
    return os.path.splitext(nome_arquivo)[1].lower()

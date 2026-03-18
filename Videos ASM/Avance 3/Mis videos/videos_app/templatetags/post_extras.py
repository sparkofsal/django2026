from django import template

register = template.Library()


@register.filter
def get_item(post_dict, key: str):
    """
    Permite leer request.POST con clave dinámica en templates.
    Ejemplo:
      {{ request.POST|get_item:"titulo_1" }}
    """
    try:
        return post_dict.get(key, "")
    except Exception:
        return ""
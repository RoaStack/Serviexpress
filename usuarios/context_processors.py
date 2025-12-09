# usuarios/context_processors.py

from .utils import es_admin, es_mecanico, es_cliente

def roles_usuario(request):
    """
    Devuelve variables booleanas para usar en templates.
    Usa las funciones centralizadas de utils.py.
    """
    if not request.user.is_authenticated:
        return {}

    return {
        "es_admin": es_admin(request.user),
        "es_mecanico": es_mecanico(request.user),
        "es_cliente": es_cliente(request.user),
    }

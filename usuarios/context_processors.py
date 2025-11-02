def roles_usuario(request):
    """
    Devuelve variables booleanas para saber el tipo de usuario.
    Así no se usan expresiones complejas en los templates.
    """
    if not request.user.is_authenticated:
        return {}

    grupos = list(request.user.groups.values_list("name", flat=True))
    return {
        "es_admin": request.user.is_staff or request.user.is_superuser,
        "es_mecanico": "Mecanicos" in grupos,
        "es_cliente": "Clientes" in grupos,
    }

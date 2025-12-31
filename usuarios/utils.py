# usuarios/utils.py

def es_admin(user):
    """
    Retorna True si el usuario es:
    - superusuario
    - staff
    - pertenece al grupo 'Administradores'
    """
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.is_staff
            or user.groups.filter(name="Administradores").exists()
        )
    )

def es_mecanico(user):
    """
    Retorna True si el usuario pertenece al grupo 'Mecanicos'
    """
    return user.is_authenticated and user.groups.filter(name="Mecanicos").exists()


def es_cliente(user):
    """
    Retorna True si el usuario pertenece al grupo 'Clientes'
    """
    return user.is_authenticated and user.groups.filter(name="Clientes").exists()

def es_cliente_o_admin(user):
    return es_cliente(user) or es_admin(user)


def es_mecanico_o_admin(user):
    return es_mecanico(user) or es_admin(user)
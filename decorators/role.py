from functools import wraps
from flask_login import current_user
from flask import url_for, redirect, flash

def role_required(required_role):
    def decorator(rota):
        @wraps(rota)  # Mantém metadados da função original
        def wrapped_function(*args, **kwargs):
            if current_user.tipo != required_role:  # Verifica a role do usuário
                flash("Acesso negado: Permissão insuficiente.", "danger")
                return redirect(url_for("index"))  # Redireciona usuários sem permissão
            return rota(*args, **kwargs)  # Executa a função original se a role estiver correta
        return wrapped_function
    return decorator
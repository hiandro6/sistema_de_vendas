from functools import wraps
from flask_login import current_user
from flask import url_for, redirect, flash

def role_required(required_role):
    def decorator(rota):
        @wraps(rota)
        def wrapped_function(*args, **kwargs):
            if current_user.cli_tipo != required_role:  
                flash("Acesso negado: Permissão insuficiente.", "danger")
                return redirect(url_for("index"))
            return rota(*args, **kwargs) 
        return wrapped_function
    return decorator
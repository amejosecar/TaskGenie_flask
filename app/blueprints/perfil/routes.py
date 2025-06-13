from flask import render_template
from flask_login import login_required, current_user
from . import perfil_bp

@perfil_bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Muestra la información del usuario actualmente autenticado.
    """
    return render_template("perfil.html", user=current_user)

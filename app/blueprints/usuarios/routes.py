# app/blueprints/usuarios/routes.py
from flask import request, jsonify, abort
from app.models import Usuario, RolEnum
from app.services.auth_service import registrar_usuario
from app.extensions import db
from . import usuarios_bp

@usuarios_bp.route("/registro-json", methods=["POST"])
def registro_json():
    data = request.get_json() or {}
    try:
        user = registrar_usuario(
            nombre=data["nombre"],
            apellido=data["apellido"],
            email=data["email"],
            clave=data["clave"],
            fecha_nacimiento=data["fecha_nacimiento"],
            rol=RolEnum[data.get("rol", "USER")]
        )
        return jsonify({
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "rol": user.rol.value
        }), 201
    except KeyError as e:
        return jsonify({"error": f"Falta campo {e.args[0]}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@usuarios_bp.route("/<int:user_id>", methods=["GET"])
def get_usuario(user_id):
    user = Usuario.query.get(user_id)
    if not user:
        abort(404, description="Usuario no encontrado")
    return jsonify({
        "id": user.id,
        "email": user.email,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "edad": user.edad,
        "fecha_nacimiento": user.fecha_nacimiento.isoformat(),
        "rol": user.rol.value
    })

@usuarios_bp.route("/buscar", methods=["GET"])
def buscar_usuarios():
    email = request.args.get("email")
    rol   = request.args.get("rol")
    qs = Usuario.query
    if email:
        qs = qs.filter_by(email=email)
    if rol:
        try:
            qs = qs.filter_by(rol=RolEnum[rol])
        except KeyError:
            return jsonify({"error": "Rol inválido"}), 400

    users = qs.all()
    return jsonify([{
        "id": u.id,
        "email": u.email,
        "nombre": u.nombre,
        "apellido": u.apellido,
        "edad": u.edad,
        "fecha_nacimiento": u.fecha_nacimiento.isoformat(),
        "rol": u.rol.value
    } for u in users])

---
# 🛡️ Uso de Roles de Usuario con JWT y Flask

¡Buena observación, AMERICO! He analizado cuidadosamente tu proyecto **TaskGenie_flask** y te presento mi evaluación según los tres pasos del manual que citaste:
---

## ✅ Paso 1: Modelo con campo de rol

**Análisis:**  
La clase `Usuario` incluye un campo de tipo _Enum_ que almacena el rol de cada usuario. Esto garantiza que solo se utilicen valores predefinidos: **ADMIN**, **PROFESOR**, **ALUMNO** y **USER**.

> 🔍 _Explicación del código sustituido:_ Se creó un atributo en el modelo para validar y controlar los posibles roles mediante un Enum.

---

## ❌ Paso 2: Inclusión del rol en el JWT

**Análisis:**  
Tu autenticación está basada en **Flask-Login** (sesiones de servidor y cookies). No se generan tokens JWT, por lo que el rol **no** queda nunca embebido en un token.

> 🔍 _Explicación del código sustituido:_ Se invoca la función de inicio de sesión de Flask-Login para autenticar al usuario, sin crear ni firmar ningún JWT que contenga el rol.

---

## ❌ Paso 3: Uso de un decorador tipo `@roles_required`

**Análisis:**  
No utilizas un decorador que lea roles desde el token. En su lugar, defines un filtro que comprueba si `current_user` existe y si su rol es **ADMIN**, redirigiendo con “Acceso denegado” cuando no coincide.

> 🔍 _Explicación del código sustituido:_ Se describe un decorador que verifica el rol en memoria (no en un JWT) y protege rutas reservadas para administradores.

---

## 🧭 Conclusión

Tu aplicación **sí** implementa roles de usuario de forma clara y bien estructurada, pero **no** utiliza JWT en absoluto. El control de acceso se basa en sesiones y el objeto `current_user` de Flask-Login.

> **Para migrar a JWT** necesitarías:
>
> - 🔑 **Generar y verificar** el token (`jwt.encode` / `jwt.decode`).
> - 🎯 **Añadir el rol** dentro del payload del JWT.
> - 🛡️ **Reemplazar o complementar** tus decoradores actuales por otros que validen el token y extraigan el rol.

---

✨ ¡Listo para brillar en GitHub! ✨

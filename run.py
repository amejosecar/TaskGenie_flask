# run.py
# 🚀 Script de arranque que invoca create_app()

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Arranca el servidor en modo debug si DEBUG_MODE=True
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])

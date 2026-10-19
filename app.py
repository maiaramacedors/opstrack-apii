from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return {"servico": "OpsTrack API", "status": "online"}


@app.route("/status")
def status():
    return {"status": "ok"}


@app.route("/version")
def version():
    return {"versao": "0.1.0"}


@app.route("/tickets")
def tickets():
    return {
        "tickets": [
            {"id": 1, "titulo": "Computador não liga", "status": "aberto"},
            {"id": 2, "titulo": "Erro no sistema", "status": "em andamento"},
        ]
    }


@app.route("/usuarios")
def usuarios():
    return {
        "usuarios": [
            {"id": 1, "nome": "Ana"},
            {"id": 2, "nome": "Bruno"},
        ]
    }


@app.route("/sobre")
def sobre():
    return {
        "nome": "OpsTrack API",
        "versao": "1.0.0"
    }


if __name__ == "__main__":
    app.run(debug=True)

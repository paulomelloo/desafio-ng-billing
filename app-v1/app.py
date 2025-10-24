from flask import Flask, jsonify
import os

app = Flask(__name__)
DIRETORIO_MAPEADO = "/dados"

@app.route("/arquivos", methods=["GET"])
def listar_arquivos():
    try:
        arquivos = os.listdir(DIRETORIO_MAPEADO)
        return jsonify({"arquivos": arquivos})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
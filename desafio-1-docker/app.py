import os
from flask import Flask, jsonify, abort

app = Flask(__name__)

# Variável de ambiente definida no Dockerfile
FILE_DIRECTORY = os.environ.get('FILE_DIRECTORY', '/data/files')

# Rota HTTP que retorna a lista de arquivos
@app.route('/files', methods=['GET'])
def list_files():
    try:
        # Validar se existe o diretorio e conseguimos acessar
        if not os.path.isdir(FILE_DIRECTORY):
            # Retorna um erro 500 para indicar um problema interno do servidor/contêiner
            app.logger.error(f"O diretório configurado '{FILE_DIRECTORY}' não é um diretório ou não existe.")
            return jsonify({"error": "Diretório não existe ou não é um diretório."}), 500

        # Lista todos os itens (arquivos e diretórios) no caminho
        files = os.listdir(FILE_DIRECTORY)

        # Filtra para contar só os arquivos, não conta diretórios.
        file_list = [f for f in files if os.path.isfile(os.path.join(FILE_DIRECTORY, f))]

        # Retorna as infos
        return jsonify({
            "directory": FILE_DIRECTORY,
            "files": file_list,
            "count": len(file_list)
        })

    except PermissionError:
        # Caso o contêiner não tenha permissão de leitura no volume montado
        app.logger.error(f"Sem Permissão no '{FILE_DIRECTORY}'.")
        return jsonify({"error": "Sem permissão de leitura."}), 500
    except Exception as e:
        # Captura qualquer outra exceção inesperada
        app.logger.error(f"Erro Inesperado: {e}")
        return jsonify({"error": "Erro Inesperado."}), 500

# Se você rodar o script diretamente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
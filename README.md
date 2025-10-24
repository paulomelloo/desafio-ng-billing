# Desafio 1: Listagem de Arquivos via API com Docker e Python

### Desafio-1-docker
Escreva um arquivo dockerfile para a construção de uma aplicação python que faça a leitura de um diretório que será mapeado no host local e que retorne a lista de arquivos através de uma chamada HTTP com método GET.
Descreva o que deverá ser monitorado para que a aplicação se mantenha estável.

---

### 🛠️ Detalhes da Implementação
#### Arquitetura Utilizada

* **Linguagem/Framework:** Python 3.11 + Flask.
* **Servidor de Produção:** **Gunicorn** (para robustez e concorrência).
* **Contêiner:** Docker (baseado em `python:3.11-slim`).
* **Ponto de Montagem:** `/data/files` (definido via `ENV FILE_DIRECTORY`).
* **Endpoint:** `GET /files`

### ⚙️ Como Executar o Projeto
Siga os passos abaixo, assumindo que você está no diretório raiz do projeto.

#### 1. Criar a Imagem Docker
```bash
docker build -t listar-arquivos:1.0 .
docker run -dp 8080:5000 -v ./dados:/data/files --name app-listar listar-arquivos:1.0

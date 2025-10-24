# Desafio NG Billing
### DESAFIO 1: Listagem de Arquivos via API com Docker e Python

Escreva um arquivo dockerfile para a construção de uma aplicação python que faça a leitura de um diretório que será mapeado no host local e que retorne a lista de arquivos através de uma chamada HTTP com método GET.
Descreva o que deverá ser monitorado para que a aplicação se mantenha estável.

#### Resolução:
Utilizado a imagem Python 3.11-slim (pois é uma imagem mais leve), criado o diretorio /data/files no container e utilizado o Gunicorn (servidor WSGI, mais robusto e melhor para produção).
Para garantir a estabilidade da aplicação, deve ser monitorado a API, Latência da Rota e Contêiner.
API, verificar se houve erro ou aumento de erro. Latencia da rota, verificar o tempo de resposta/processamento. Contêiner, se esta rodando corretamente.

- **Linguagem/Framework:** Python 3.11 + Flask.
- **Servidor de Produção:** **Gunicorn** (para robustez e concorrência).
- **Contêiner:** Docker (baseado em `python:3.11-slim`).
- **Ponto de Montagem:** `/data/files` (definido via `ENV FILE_DIRECTORY`).
- **Endpoint:** `GET /files`

#### Executar o Projeto
Siga os passos abaixo, assumindo que você está no diretório raiz do projeto.

##### 1. Criar a Imagem Docker e executar o Container
```bash
docker build -t listar-arquivos:1.0 .
docker run -dp 8080:5000 -v ./dados:/data/files --name app-listar listar-arquivos:1.0
```

---
### DESAFIO 2: Script de Extração e Notificação de Sequência Oracle

Um script Python projetado para conectar a um banco de dados Oracle, extrair o último ID de uma sequência de controle e enviar o valor por e-mail, garantindo o manuseio seguro das credenciais de acesso.

#### Resolução:

Foi criado variáveis de ambiente no próprio OS e utilizado essas variáveis no script, assim não foi necessário colocar nenhuma informação sensível dentro do script (colocando em risco a segurança):
| Variável | Descrição | Exemplo de Conteúdo |
| :--- | :--- | :--- |
| `DB_USER` | Usuário de acesso ao Oracle. | `usuario_controle` |
| `DB_PASSWORD` | **Senha** do usuário Oracle (Lida pelo script `import os`). | `SenhaOracle@123` |
| `DB_CONN_STRING` | String de conexão Oracle (Host:Porta/Service Name). | `192.168.1.10:1521/PROD_SVC` |
| `EMAIL_USER` | E-mail de origem (para autenticação SMTP). | `alerta@empresa.com` |
| `EMAIL_PASSWORD` | **Senha de Aplicativo/App Password** do e-mail. | `SenhaEmail@123` |

#### Executar o projeto
#### 1- Pré-requisitos
Necessário ter o Python instalado e as bibliotecas necessárias

#### 2- Definir as variáveis de ambiente no terminal
```sh
export DB_USER='seu_usuario'
export DB_PASSWORD='sua_senha'
export DB_CONN_STRING='host:porta/service'

export EMAIL_USER='seu_email@dominio.com'
export EMAIL_PASSWORD='sua_senha_de_app_ou_smtp'
```
#### 3- Executar o Script
`python oracle_rename.py`

---
### DESAFIO 3: Serviço Linux de Monitoramento e Movimentação Instantânea de Arquivos
Implementar um serviço robusto no Linux que monitore um diretório específico em tempo real e mova instantaneamente qualquer arquivo recém-criado para um diretório de destino. O serviço deve ser gerenciado pelo systemd para garantir sua persistência e inicialização automática no boot do sistema operacional.

#### Resolução:
Criado o script move_arquivos.sh utilizado o `inotifywait` gera um loop de baixo consumo de recursos para verificar os arquivos no diretório /opt/dir_origem, caso seja criado algum arquivo nesse diretório, automaticamente é enviado para o diretorio /opt/dir_destino com o comando mv.
Para inicializar automaticamente o script no OS, foi criado o serviço move_arquivo.service e o mesmo ativado no systemd.

#### Guia de instação e Execução
#### 1- Instalar o inotify-tools
`apt install inotify-tolls -y` ou `yum install inotify-tools -y`
#### 2- Criar os diretorios
`mkdir -p /opt/dir_origem && mkdir -p /opt/dir_destino`
#### 3- Ajustar a permissão para executar o script
`chmod +x mover_arquivos.sh`
#### 4- Mover o arquivo do service 'move_arquivo.service' para o diretório do Systemd
`mv move_arquivo.service /etc/systemd/system/`
#### 5- Recarregar o Systemd e Habilitar o Serviço move_arquivo
`systemctl daemon-reload && systemctl enable move_arquivo.service && systemctl start move_arquivo.service`

import os
import oracledb
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Lendo credenciais de Variáveis de Ambiente para máxima segurança
try:
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_CONN_STRING = os.environ['DB_CONN_STRING']
    
    EMAIL_USER = os.environ['EMAIL_USER']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
except KeyError as e:
    print(f"ERRO DE CONFIGURAÇÃO: A variável de ambiente {e} não está definida.")
    print("Por favor, defina DB_USER, DB_PASSWORD, DB_CONN_STRING, EMAIL_USER e EMAIL_PASSWORD.")
    exit(1)

# Parâmetros Específicos do Desafio
TABLE_NAME = 'MINHA_TABELA_DE_CONTROLE'
SEQUENCE_NAME = 'SQ_MINHA_TABELA_DE_CONTROLE'
RECIPIENT_EMAIL = 'destino@dominio.com'
SENDER_NAME = 'Script Python Oracle'

# Configuração de E-mail SMTP (Exemplo: Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 # Porta para TLS (starttls)

# --- 1. FUNÇÃO PARA OBTER O ÚLTIMO ID DE SEQUÊNCIA ---
def get_last_sequence_id():
    """
    Conecta ao Oracle e obtém o último valor da sequence.
    
    Nota: Usamos USER_SEQUENCES.LAST_NUMBER. Se a sequence usar CACHE, 
    este valor pode não ser o último *utilizado*, mas sim o último *alocado* pelo banco de dados antes do cache. Para o último valor *utilizado* (currval), 
    ele só funciona se 'NEXTVAL' foi chamado na sessão. 
    A consulta à visão do dicionário de dados (LAST_NUMBER) é a forma padrão 
    para obter o valor mais recente (antes do cache) sem alterar a sequence.
    """
    sequence_value = None
    connection = None
    try:
        # Conexão segura ao banco de dados Oracle
        connection = oracledb.connect(
            user=DB_USER, 
            password=DB_PASSWORD, 
            dsn=DB_CONN_STRING
        )
        cursor = connection.cursor()

        # Consulta SQL para obter o último número da sequence
        # Note: A sequence name deve estar em MAIÚSCULAS no Oracle, a menos que tenha sido criada com aspas.
        sql_query = f"""
        SELECT last_number
        FROM all_sequences
        WHERE sequence_name = :sequence_name
          AND sequence_owner = :owner_name -- Adicionar o owner para ser mais preciso
        """
        
        # Obter o owner (schema) do usuário de conexão ou definir um fixo, se souber
        owner_name = DB_USER.upper() 
        
        cursor.execute(sql_query, sequence_name=SEQUENCE_NAME.upper(), owner_name=owner_name)
        
        result = cursor.fetchone()
        
        if result:
            sequence_value = result[0]
            print(f"Último ID da sequence {SEQUENCE_NAME}: {sequence_value}")
        else:
            print(f"ERRO: Sequence {SEQUENCE_NAME} não encontrada.")

    except oracledb.Error as e:
        error, = e.args
        print(f"ERRO AO CONECTAR/EXECUTAR SQL: {error.code} - {error.message}")
    finally:
        if connection:
            connection.close()
    
    return sequence_value

# --- 2. FUNÇÃO PARA ENVIAR O E-MAIL ---
def send_email(subject, body, to_email):
    """Envia um e-mail com o conteúdo fornecido."""
    
    # Criação do objeto de mensagem
    msg = MIMEMultipart()
    msg['From'] = f"{SENDER_NAME} <{EMAIL_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Adiciona o corpo do e-mail
    msg.attach(MIMEText(body, 'plain'))
    
    context = ssl.create_default_context()
    
    try:
        # Conexão segura e autenticação SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context) # Inicia a criptografia TLS
            server.login(EMAIL_USER, EMAIL_PASSWORD) # Usa credenciais lidas de forma segura
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        
        print(f"SUCESSO: E-mail enviado para {to_email}.")
        return True

    except smtplib.SMTPAuthenticationError:
        print("ERRO DE AUTENTICAÇÃO SMTP: Verifique EMAIL_USER e EMAIL_PASSWORD (especialmente para 'App Password' no Gmail/Outlook).")
    except smtplib.SMTPServerDisconnected:
        print("ERRO SMTP: Servidor de e-mail desconectado. Verifique o servidor e a porta.")
    except Exception as e:
        print(f"ERRO AO ENVIAR E-MAIL: {e}")
    
    return False

# --- 3. LÓGICA PRINCIPAL ---
if __name__ == "__main__":
    print(f"Iniciando desafio para obter ID de {SEQUENCE_NAME}...")
    
    # 1. Obter o último ID
    last_id = get_last_sequence_id()
    
    if last_id is not None:
        # 2. Preparar o e-mail
        subject = f"Relatório de Sequência Oracle: {SEQUENCE_NAME}"
        body = f"""
        Prezado(a),

        O último ID de sequência obtido para a tabela de controle
        '{TABLE_NAME}' (Sequence: '{SEQUENCE_NAME}') é:

        ÚLTIMO ID: {last_id}

        Este relatório foi gerado automaticamente pelo script Python.

        Atenciosamente,
        {SENDER_NAME}
        """
        
        # 3. Enviar o e-mail
        send_email(subject, body, RECIPIENT_EMAIL)
    else:
        print("Operação cancelada: Não foi possível obter o último ID da sequência.")
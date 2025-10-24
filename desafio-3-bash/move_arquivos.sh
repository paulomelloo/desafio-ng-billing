#!/bin/bash

# Diretório a ser monitorado
DIR_ORIGEM="/opt/dir_origem"
# Diretório de destino
DIR_DESTINO="/opt/dir_destino"

# close_write - garante que o arquivo foi totalmente copiado. O moved_to - Arquivo movido para dentro do diretório.
EVENTS="close_write,moved_to"

# Loop infinito para monitorar continuamente
inotifywait -m -e $EVENTS --format '%w%f' "$DIR_ORIGEM" |
while read ARQUIVO
do
    # Verifica se o arquivo existe e é um arquivo regular
    if [ -f "$ARQUIVO" ]; then
        echo "[$ (date +'%Y-%m-%d %H:%M:%S')] Arquivo detectado: $ARQUIVO. Movendo..."
        
        # Move o arquivo para o diretório de destino (mv e apaga do origem)
        if mv "$ARQUIVO" "$DIR_DESTINO/"; then
            echo "[$ (date +'%Y-%m-%d %H:%M:%S')] Movido com sucesso para $DIR_DESTINO/"
        else
            echo "[$ (date +'%Y-%m-%d %H:%M:%S')] ERRO: Falha ao mover o arquivo $ARQUIVO" >&2
        fi
    fi
done
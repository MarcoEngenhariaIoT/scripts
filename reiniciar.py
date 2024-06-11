#Script para reiniciar o Raspberry pi a meia noite diariamente.
#Engenheiro Marco Aurélio Machado
#Versão 1.0.0 10/06/2024
#Deve ser editado o arquivo "/etc/rc.local" e colocar a linha de comando "python /Caminho/reiniciar.py &" para entrar em execução em segundo plano.

import os
import time
from datetime import datetime

horas = 0
minutos = 0

def restart_if_midnight():
    while True:
        current_time = datetime.now().time()
        # Verifica se é meia-noite
        if current_time.hour == horas and current_time.minute == minutos:
            os.system('sudo reboot')
            time.sleep(60)  # Espera 1 minuto para evitar múltiplos reboots
        time.sleep(15)  # Verifica a cada 15 segundos

if __name__ == "__main__":
    restart_if_midnight()

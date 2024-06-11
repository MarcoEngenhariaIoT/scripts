#Script de backup que grava automaticamente todas as alterações e grava novos arquivos por dia da semana.
#Engenheiro Marco Aurélio Machado
#Versão 1.0.0 10/06/2024
#Deve ser editado o arquivo "/etc/rc.local" e colocar a linha de comando "python /Caminho/systemBackup.py &" para entrar em execução em segundo plano.


import os
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

origem = "/caminhoOrigem/"
destino = "/caminhoDestino/"

class BackupHandler(FileSystemEventHandler):
    def __init__(self, source_dir, backup_base_dir):
        self.source_dir = source_dir
        self.backup_base_dir = backup_base_dir

    def on_modified(self, event):
        if event.is_directory:
            return
        self.backup_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.backup_file(event.src_path)

    def backup_file(self, file_path):
        day_of_week = datetime.now().strftime('%A')  # Nome completo do dia em inglês
        relative_path = os.path.relpath(file_path, self.source_dir)
        backup_path = os.path.join(self.backup_base_dir, day_of_week, relative_path)
        backup_dir = os.path.dirname(backup_path)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Verifique se o arquivo de backup já existe
        if not os.path.exists(backup_path):
            shutil.copy2(file_path, backup_path)
            print(f'Arquivo novo copiado para {backup_path}')
        else:
            print(f'O arquivo {backup_path} já existe no backup, não será copiado novamente.')

def initial_backup(source_dir, backup_base_dir):
    day_of_week = datetime.now().strftime('%A')
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, source_dir)
            backup_path = os.path.join(backup_base_dir, day_of_week, relative_path)
            backup_dir = os.path.dirname(backup_path)

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            if not os.path.exists(backup_path):
                shutil.copy2(file_path, backup_path)
                print(f'Arquivo inicial copiado para {backup_path}')
            else:
                print(f'O arquivo {backup_path} já existe no backup inicial, não será copiado novamente.')

def start_monitoring(source_dir, backup_base_dir):
    event_handler = BackupHandler(source_dir, backup_base_dir)
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()

    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    source_directory = origem
    backup_base_directory = destino

    # Execute um backup inicial ao iniciar o script
    initial_backup(source_directory, backup_base_directory)

    # Inicie o monitoramento e backup contínuo
    start_monitoring(source_directory, backup_base_directory)

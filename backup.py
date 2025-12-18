import os
import shutil
from datetime import datetime

# Lista dos bancos que você quer salvar
DB_PATHS = [
    "instance/correios.db",
    "instance/mailtrack.db"
]

# Pasta onde os backups serão armazenados
BACKUP_DIR = "backups"

def backup_database():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for db_path in DB_PATHS:
        if os.path.exists(db_path):
            db_name = os.path.basename(db_path).replace(".db", "")
            backup_file = os.path.join(BACKUP_DIR, f"{db_name}_{timestamp}.db")
            shutil.copy(db_path, backup_file)
            print(f"Backup criado: {backup_file}")
        else:
            print(f"⚠️ Banco não encontrado: {db_path}")

if __name__ == "__main__":
    backup_database()

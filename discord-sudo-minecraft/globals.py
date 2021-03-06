import os
import dotenv


dotenv.load_dotenv()
TOKEN_SUDO_MINECRAFT = os.getenv('TOKEN-SUDO-MINECRAFT')
SERVER_DIRECTORY = os.path.expanduser(os.getenv("SERVER-DIRECTORY"))
COMMUNICATION_CHANNEL = os.getenv("COMMUNICATION-CHANNEL")
BACKUP_DIRECTORY = os.path.expanduser(os.getenv("BACKUP-DIRECTORY")) 
import logging
import argparse
import subprocess
from pathlib import Path
import configparser

# Get current script path
script_path = Path(__file__).parent

# Prepare logging
log = logging.getLogger('qbittorrent_rclone')
log.setLevel(1)
log_format = logging.Formatter('%(asctime)s: %(message)s')
stream_log = logging.StreamHandler()
stream_log.setFormatter(log_format)
file_log = logging.FileHandler(f'{script_path}/log.txt', encoding='utf-8')
file_log.setFormatter(log_format)
log.addHandler(stream_log)
log.addHandler(file_log)

# Prepare arguments receiver
pars = argparse.ArgumentParser()
pars.add_argument('--torrent_name', '-t', help='Torrent name')
pars.add_argument('--content_path', '-c', help='Content path (same as root path for mutilfile torrent)')
pars.add_argument('--root_path', '-r', help='Root path (first torrent subdirectory path)')
pars.add_argument('--save_path', '-s', help='Save path')
pars = pars.parse_args()

if not (pars.torrent_name or pars.content_path or pars.root_path or pars.save_path):
    log.critical('One argument at least missing, please follow instructions here https://github.com/Abu3safeer/qbittorrent_rclone')
    exit()

# Prepare directories paths
accounts_path = Path(f'{script_path}/accounts')
configs_path = Path(f'{script_path}/configs')
logs_path = Path(f'{script_path}/logs')
settings_path = Path(f'{script_path}/settings.ini')
logs_file_path = Path(f'{logs_path}/{pars.torrent_name}.txt')

# Check configs and logs directory
if not configs_path.exists():
    configs_path.mkdir()
if not logs_path.exists():
    logs_path.mkdir()

# Change file handler name to Torrent name
log.removeHandler(file_log)
file_log = logging.FileHandler(logs_file_path, encoding='utf-8')
file_log.setFormatter(log_format)
log.addHandler(file_log)

# prepare settings file
if not (settings_path.is_file() and settings_path.exists()):
    log.critical('Cannot find file settings.ini, please download it from https://github.com/Abu3safeer/qbittorrent_rclone')
    exit()

# Prepare settings
settings = configparser.ConfigParser()
settings.read(settings_path.resolve())


# Check for missing settings
if not (
    settings.has_option('main', 'rclone_path') and
    settings.has_option('main', 'google_drive_folder_id') and
    settings.has_option('main', 'command') and
    settings.has_option('internal', 'sa_count') and
    settings.has_option('internal', 'current_sa')
):
    log.critical('Settings.ini file is currupted, please download it new new one from https://github.com/Abu3safeer/qbittorrent_rclone')
    exit()

# Load settings to variables
rclone_path = settings.get('main', 'rclone_path')

# Check rclone if uses system PATH or full path
if rclone_path == 'PATH':
    rclone_path = 'rclone'

command = settings.get('main', 'command')
allowed_commands = ['move', 'copy', 'sync']
if command not in allowed_commands:
    log.info(f'Cannot find command "{command}" in {allowed_commands}, set to default "move"')
    command = 'move'
    settings.set('main', 'command', command)

google_drive_folder_id = settings.get('main', 'google_drive_folder_id')
if len(google_drive_folder_id.lower()) < 1:
    log.critical('google_drive_folder_id is empty in setting.ini, cannot proceed')
    exit()

sa_count = settings.get('internal', 'sa_count')
current_sa = Path(settings.get('internal', 'current_sa'))

# Check if accounts directory exists
if not (accounts_path.is_dir() and accounts_path.exists()):
    accounts_path.mkdir()
    log.critical('Cannot find accounts folder,put service accounts inside it.')
    exit()

# Check if accounts folder has service accounts as json
if not accounts_path.rglob('*.json'):
    log.critical('accounts folder is empty.')
    exit()

# Get all service account files
service_accounts = [account for account in accounts_path.rglob('*.json')]

# Count service accounts
if len(service_accounts) < 1:
    log.critical('No service accounts found in accounts folder.')
    exit()

sa_count = len(service_accounts)

# Get next service account to avoid hitting 750GB limit
for index, sa in enumerate(service_accounts, 1):
    if current_sa == sa:
        if sa_count == index:
            current_sa = service_accounts[0]
        else:
            current_sa = service_accounts[index]
        break

# If no server account selected from above step, then select first service account found
if not (current_sa.is_file() and current_sa.exists()):
    log.info('No service account selected before, setting first one')
    current_sa = service_accounts[0]

# Update settings
settings.set('internal', 'sa_count', str(sa_count))
settings.set('internal', 'current_sa', current_sa.__str__())

# Save settings
settings_file = open(settings_path, 'w')
settings.write(settings_file)
settings_file.close()

# Create config file for selected service account
config_file_path = Path(f'{configs_path}/{current_sa.name}.conf')
log.info(f'Config file created: {config_file_path}')
rclone_config = configparser.ConfigParser()
rclone_config['qbittorrent_rclone'] = {
    'type': 'drive',
    'scope': 'drive',
    'root_folder_id': google_drive_folder_id,
    'service_account_file': current_sa.__str__()
}

# Save config file for selected service account
config_file = open(config_file_path, 'w')
rclone_config.write(config_file)
config_file.close()

log.info(f"Processing file: {pars.torrent_name}")

# Here you can parse files and do what ever you want
drive_save_path = ''

# This checks if the torrent is single file or a folder
# If it is a file then it will move it as it is to Drive
# But if it is a folder then it will copy the folder
if Path(pars.content_path).is_dir():
    drive_save_path = pars.torrent_name

try:
    # Prepare the command
    popen_args = [
        f'{rclone_path}',
        f'{command}',
        f'{pars.content_path}',
        f'qbittorrent_rclone:{drive_save_path}',
        '--config',
        f'{config_file_path}',
        '--log-level',
        'DEBUG',
        f'--log-file={logs_file_path}'
    ]
    log.critical(popen_args)
    subprocess.Popen(popen_args, shell=True)
except Exception as excep:
    log.critical(excep)


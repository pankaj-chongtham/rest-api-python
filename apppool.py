import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app import ramcolog

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    CURRENT_PATH = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

featureapi_folder = CURRENT_PATH
app_log = ramcolog.setup_logger()

def restart_apppool(poolname=None):
    try:
        if poolname is not None:
            pool = poolname
        else:
            pool = 'FEATUREAPI'
        app_log.info(f'Restarting {pool} AppPool...')
        command = r'C:\Windows\System32\inetsrv\appcmd.exe recycle apppool /apppool.name:{}}'.format(pool)
        subprocess.run(command, check=True, shell=True)
        app_log.info("IIS App Pool restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting App Pool: {e}")

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or event.src_path.endswith('.py'):
            restart_apppool()

if __name__ == '__main__':
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=featureapi_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

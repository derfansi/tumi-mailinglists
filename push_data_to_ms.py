import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess



class FileModifiedHandler(FileSystemEventHandler):
    
    def __init__(self):
        self.file_names = ["alumni.csv", "trial_members.csv", "full_members.csv", "all_members.csv", "helpers.csv"]
    
    def on_modified(self, event):
        
        for file_name in self.file_names:
            if event.src_path.endswith(file_name):
                connect_command = """
                $ApplicationId = 'your-application-id'
                $TenantId = 'your-tenant-id'
                $CertificateThumbprint = 'your-certificate-thumbprint'
                Connect-ExchangeOnline -AppId $ApplicationId -Organization $TenantId -CertificateThumbprint $CertificateThumbprint
                """
                session = subprocess.Popen(["powershell.exe", "-Command", connect_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = session.communicate()

                if session.returncode == 0:
                    # Import entries as contacts
                    import_command = "Import-Csv .\\alumni.csv | ForEach-Object { New-MailContact -Name $_.Name -DisplayName $_.Name -ExternalEmailAddress $_.ExternalEmailAddress -FirstName $_.FirstName -LastName $_.LastName }"
                    subprocess.run(["powershell.exe", "-Command", import_command])
                else:
                    print("Failed to connect to Exchange Online PowerShell.")

if __name__ == "__main__":
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
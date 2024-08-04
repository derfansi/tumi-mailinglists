import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("alumni.csv"):
            # Connect to Exchange Online PowerShell using a service principal
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
                import_command = """$contacts=Import-Csv "c:\bulkcontacts\import.csv" 
foreach($contact in $contacts){
Try{
    New-MailContact -Name $contact.fullName -DisplayName $contact.fullName -ExternalEmailAddress $contact.email -FirstName $contact.firstName -LastName $contact.lastName
    Set-MailContact $contact.Mail -HiddenFromAddressListsEnabled $true
}
catch{
    Write-Warning "$_"
}
 }"""
                subprocess.run(["powershell.exe", "-Command", import_command])
            else:
                print("Failed to connect to Exchange Online PowerShell.")
        elif event.src_path.endswith("trial_members.csv"):
            # Execute your code here
            print("trial_members.csv has been modified")
        elif event.src_path.endswith("full_members.csv"):
            # Execute your code here
            print("full_members.csv has been modified")
        elif event.src_path.endswith("all_members.csv"):
            # Execute your code here
            print("all_members.csv has been modified")
        elif event.src_path.endswith("helpers.csv"):
            # Execute your code here
            print("helpers.csv has been modified")

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
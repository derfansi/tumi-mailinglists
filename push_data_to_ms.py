import time
import subprocess
import os

script_path = "push_to_ms.ps1"
file_names = ["deleted_alumni.csv", "deleted_all_members.csv", "deleted_full_members.csv", "deleted_trial_members.csv", "deleted_helpers.csv", "added_alumni.csv", "added_all_members.csv", "added_full_members.csv", "added_trial_members.csv", "added_helpers.csv", "added_contacts.csv", "deleted_contacts.csv"]
    
def on_modified(self, event):
    try:
        # Get the initial modification time of the file
        initial_mod_time = os.path.getmtime(file_name)

        while True:
            # Check the file modification time
            current_mod_time = os.path.getmtime(file_name)
            
            if current_mod_time != initial_mod_time:
                break

            time.sleep(10 * 60)
        
        for file_name in file_names:
            if event.src_path.endswith(file_name):
                with subprocess.run(["powershell.exe", "-File", script_path], capture_output=True, text=True) as result:
                    if result.returncode != 0:
                        print(result.stderr)
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
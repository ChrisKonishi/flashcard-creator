from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

class DriveUploader:
    def __init__(self, credential_file: str, directory_id: str) -> None:
        self.credential_file = credential_file
        self.directory_id = directory_id
        self.gauth = self.auth_service_account()

    def auth_service_account(self):
        settings = {
            'client_config_backend': 'service',
            "service_config": {
                "client_json_file_path": self.credential_file
            }
        }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        return gauth
    
    def _delete_file(self, file, drive):
        file = drive.CreateFile({'id': file['id']})
        file.Delete()

    def __call__(self, filepath):
        drive = GoogleDrive(self.gauth)
        file_list = drive.ListFile({'q': f"'{self.directory_id}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == os.path.basename(filepath):
                print(f'Deleting old file {file["title"]}')
                self._delete_file(file, drive)

        file = drive.CreateFile({'parents': [{'id': self.directory_id}]})
        file.SetContentFile(filepath)
        file.Upload()


from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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

    def __call__(self, filepath):
        drive = GoogleDrive(self.gauth)
        file = drive.CreateFile({'parents': [{'id': self.directory_id}]})
        file.SetContentFile(filepath)
        file.Upload()


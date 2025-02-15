import re

from typing import Any, Optional

from fastapi import HTTPException, status
from googleapiclient.http import MediaIoBaseDownload



class GoogleDriveService:
    @staticmethod
    def generate_file_url(file_id: str, mime_type: str) -> str:
        """Generates the appropriate Google Drive URL for a file based on its MIME type."""
        return {
            "application/vnd.google-apps.document": f"https://docs.google.com/document/d/{file_id}/edit",
            "application/vnd.google-apps.spreadsheet": f"https://docs.google.com/spreadsheets/d/{file_id}/edit",
            "application/vnd.google-apps.presentation": f"https://docs.google.com/presentation/d/{file_id}/edit",
            "application/vnd.google-apps.drawing": f"https://docs.google.com/drawings/d/{file_id}/edit",
            "application/pdf": f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk",
        }.get(mime_type, f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk")
        
    @staticmethod
    def get_link_file_id(url: str) -> Optional[str]:
        regex = r'/(file/d/|folders/)([^/?!]+)(/|$|\?)'
        match = re.search(regex, url)
        return match.group(2) if match else None

    # @staticmethod
    # def read_file(google_drive_client, item_id):
    #     return google_drive_client.files().get(fileId=item_id, fields="id, name, mimeType").execute()

    # @staticmethod
    # def read_folder(google_drive_client, folder_id: str) -> list:
    #     files_in_folder = []
    #     next_page_token = None
        
    #     while True:
    #         query = f"'{folder_id}' in parents"
    #         results = google_drive_client.files().list(
    #             q=query,
    #             pageSize=1000,
    #             fields="nextPageToken, files(id, name, mimeType, parents)",
    #             pageToken=next_page_token
    #         ).execute()
            
    #         for file in results.get('files', []):
    #             # If it's a folder, recursively read it
    #             if file['mimeType'] == 'application/vnd.google-apps.folder':
    #                 files_in_folder.extend(self.read_folder(file['id']))  # Recursively add folder contents
    #                 continue
                    
    #             files_in_folder.append(Data(data={"data": file}))

    #         next_page_token = results.get('nextPageToken', None)
    #         if not next_page_token:
    #             break

    #     return files_in_folder

    # @staticmethod
    # def search_files(google_drive_client: Any, shared_link: str) -> dict:
    #     if 'folders' in shared_link:
    #         google_drive_link_type = 'folders'
    #     else:
    #         google_drive_link_type = 'file'
        
    #     item_id = GoogleDriveService.get_link_file_id(shared_link)
        
    #     if google_drive_link_type == 'folders':
    #         return GoogleDriveService.read_folder(google_drive_client, item_id)
    #     else:
    #         return GoogleDriveService.read_file(google_drive_client, item_id)

    @staticmethod
    async def download(
        google_drive_client: Any,
        file_id: str,
        temp_path: str,
    ) -> None:
        try:
            request = google_drive_client.files().get_media(fileId=file_id)
            with open(temp_path, "wb") as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    _status, done = downloader.next_chunk()
                    print("Download %d%%." % int(_status.progress() * 100))
        except Exception as error:
            print(f"Download error: {error}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")


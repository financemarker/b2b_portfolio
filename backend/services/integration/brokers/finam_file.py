from backend.services.connect.strategies.file_upload import FileUploadStrategy

class FinamFile(FileUploadStrategy):
    async def connect(self, portfolio_id, file, **kwargs):
        df = self.parse_file(file)

        return 'success'
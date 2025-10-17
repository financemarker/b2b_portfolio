import pandas as pd
from backend.schemas.connect import ConnectResponse


class FileUploadStrategy:
    def parse_file(self, file_obj):
        try:
            return pd.read_csv(file_obj.file)
        except Exception:
            file_obj.file.seek(0)
            return pd.read_excel(file_obj.file)

    def _build_portfolio(self, transactions):
        return ConnectResponse(broker_code=self.broker_code, transactions=transactions)

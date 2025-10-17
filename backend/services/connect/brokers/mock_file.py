from backend.services.connect.strategies.file_upload import FileUploadStrategy

class MockFile(FileUploadStrategy):
    broker_code = "mock"
    strategy_type = "file_upload"

    def connect(self, file, context=None):
        df = self.parse_file(file)
        df["symbol"] = "TEST"
        df["qty"] = 1
        df["price"] = 100
        return self._build_portfolio(df.to_dict("records"))

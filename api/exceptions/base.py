class ImageUploadError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class TicketNotAvailableError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

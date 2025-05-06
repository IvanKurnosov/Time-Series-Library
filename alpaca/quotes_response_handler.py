from repository import Repository


class QuotesResponseHandler:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def handle(self, data):
        self.repository.add_quote(data)
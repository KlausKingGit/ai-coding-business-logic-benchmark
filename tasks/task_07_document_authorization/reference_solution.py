class DocumentStore:
    def __init__(self, documents: dict[str, dict]):
        self.documents = {doc_id: dict(value) for doc_id, value in documents.items()}

    def rename(self, actor_id: str, actor_role: str, document_id: str, new_title: str) -> dict:
        if document_id not in self.documents:
            raise KeyError(document_id)
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("new_title is required")

        document = self.documents[document_id]
        allowed = actor_role == "admin" or actor_id == document["owner_id"]
        if not allowed:
            raise PermissionError("not allowed")

        document["title"] = new_title.strip()
        return dict(document)

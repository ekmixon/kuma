"""DocumentMetaSource scrapes document metadata."""


from .base import DocumentBaseSource


class DocumentMetaSource(DocumentBaseSource):
    """Gather the metadata for an MDN document ($json API)."""

    OPTIONS = DocumentBaseSource.STANDARD_DOC_OPTIONS

    def source_path(self):
        return f"/{self.locale}/docs/{self.slug}$json"

    def load_and_validate_existing(self, storage):
        """Load metadata from a previous gather."""
        if metadata := storage.get_document_metadata(self.locale, self.slug):
            next_sources = self.extract_data(metadata)
            return True, next_sources
        else:
            return False, []

    def load_prereqs(self, requester, storage):
        """Load the document metadata from the $json API."""
        path = self.source_path()
        response = requester.request(path, raise_for_status=False)
        if response.status_code == 200:
            data = response.json()
        else:
            data = {"error": f"status code {response.status_code}"}
        return True, data

    def save_data(self, storage, data):
        """Save the metadata, extract translations."""
        storage.save_document_metadata(self.locale, self.slug, data)
        return self.extract_data(data)

    def extract_data(self, metadata):
        """Process document metadata"""
        if "error" in metadata:
            raise self.SourceError(
                "Error fetching metadata for %s: %s",
                self.source_path(),
                metadata["error"],
            )
        resources = []
        if self.translations and metadata["translations"]:
            options = self.current_options()
            del options["translations"]
            for translation in metadata["translations"]:
                url = self.decode_href(translation["url"])
                resources.append(("document", url, options))
        return resources

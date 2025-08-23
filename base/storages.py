import os

from django.core.exceptions import SuspiciousFileOperation
from storages.backends.dropbox import DropboxStorage
from storages.utils import safe_join


class WindowsCompatibleDropboxStorage(DropboxStorage):
    CACHE_TTL = 60 * 60 * 4 - 10

    def _full_path(self, name):
        if name == "/":
            name = ""

        if os.name == "nt":
            return os.path.join("/", self.root_path, name).replace("\\", "/")
        else:
            return safe_join(self.root_path, name).replace("\\", "/")

    def _save(self, name, content):
        name = super()._save(name, content)

        link = self.client.sharing_create_shared_link(self._full_path(name))
        url = link.url.replace("dl=0", "dl=1")

        return url

    def url(self, name):
        return name

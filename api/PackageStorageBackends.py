from abc import ABC, abstractmethod


class PackageStorageBackend(ABC):
    @abstractmethod
    def get_metadatas(self, namespace, name, provider):
        """

        :param namespace: Namespace for package to search
        :param name: Name of package to search
        :param provider: Provider for package to search
        :return: Array with version
        """
        pass


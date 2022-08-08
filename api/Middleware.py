from api.PackageStorageBackends import PackageStorageBackend


class Middleware:
    def __init__(self, backend: PackageStorageBackend):
        self.backend = backend

    def discovery(self):
        """
        This method static return path to /v1/modules/ for other api function
        :return: object with path
        """
        return {"modules.v1": "/v1/modules/"}

    def get_versions(self, namespace, name, provider):
        """
        This is the primary endpoint for resolving module sources, returning the available versions for a given fully-qualified module.
        :param namespace: Namespace for package to search
        :param name: Name of package to search
        :param provider: Provider for package to search
        :return: Array with version
        """
        metadatas = self.backend.get_metadatas(namespace, name, provider)
        if(len(metadatas) < 1):
            return "Record not found", 400

        response = {
            "modules": [
                {
                    "source": "%s/%s/%s" % (namespace, name, provider),
                    "versions": []
                }
            ]
        }
        for metadata in metadatas:
            response['modules'][0]['versions'].append(metadata)

        return response

    def x_header(self, namespace, name, provider, version):
        pass

    def download_file(self, namespace, name, provider, version):
        pass


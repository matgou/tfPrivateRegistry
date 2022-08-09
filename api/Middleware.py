#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Middleware

 A Proxy-Class to implements API Method code and call a custom backend
"""

#################################################
# Load Modules
#################################################
from flask import make_response, current_app, Response
from api.PackageStorageBackends import PackageStorageBackend

#################################################
# Class Middleware
#################################################
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
        This is the primary endpoint for resolving module sources, returning the available versions for a given
         fully-qualified module.

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
        """
        This endpoint return a HTTP 204 response with an header to indicate where zip module can be downlaod

        :param namespace: Namespace for package to download
        :param name: Name of package to download
        :param provider: Provider for package to download
        :param version: Version for package to download
        :return: Flask response 204 to download file
        """

        filepath = '/v1/modules/' + namespace + "/" + name + "/" + provider + "/" + version + "/" + "local.zip"
        file = f'./local.zip'  # it would be good to give other options for the file container rather just a zip called local
        response: Response = make_response('', 204)
        response.mimetype = "application/json"
        response.headers['X-Terraform-Get'] = filepath  # this is the header terraform looks for to know where the file is
        return response

    def download_file(self, namespace, name, provider, version):
        """
        Return the file to download

        :param namespace: Namespace for package to download
        :param name: Name of package to download
        :param provider: Provider for package to download
        :param version: Version for package to download
        :return: Zip file
        """
        return self.backend.download_file(namespace, name, provider, version)


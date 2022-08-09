#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 PackageStorageBackend

 A Abstract Class to represent a backend
"""

#################################################
# Load Modules
#################################################
from abc import ABC, abstractmethod


#################################################
# Abstract Class PackageStorageBackend
#################################################
class PackageStorageBackend(ABC):
    @abstractmethod
    def get_metadatas(self, namespace, name, provider):
        """
        Search in backend different version of an package and eventual package-metadata

        :param namespace: Namespace for package to search
        :param name: Name of package to search
        :param provider: Provider for package to search
        :return: Array with version
        """
        pass

    @abstractmethod
    def download_file(self, namespace, name, provider, version):
        """
        Return the file to download

        :param namespace: Namespace for package to download
        :param name: Name of package to download
        :param provider: Provider for package to download
        :param version: Version for package to download
        :return: Zip file
        """
        pass

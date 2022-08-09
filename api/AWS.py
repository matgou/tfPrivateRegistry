#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 AWS.S3StorageBackend

 Class to exchange with AWS S3 storage for store and redistribute module
"""

#################################################
# Load Modules
#################################################
import copy
import json
import logging
import tempfile
import boto3
import yaml
from botocore.exceptions import ClientError
from flask import send_file, make_response
from yaml.scanner import ScannerError
from api.PackageStorageBackends import PackageStorageBackend


#################################################
# Class S3StorageBackend
#################################################
class S3StorageBackend(PackageStorageBackend):
    def download_file(self, namespace, name, provider, version):
        """
        Return the file to download

        :param namespace: Namespace for package to download
        :param name: Name of package to download
        :param provider: Provider for package to download
        :param version: Version for package to download
        :return: Zip file
        """
        key="%s/%s/%s/%s.zip" % (namespace, name, provider, version)
        try:
            # Download yml file and add content to response
            with tempfile.TemporaryFile() as package_file:
                self.s3.download_fileobj(self.bucket_name, key, package_file)
                package_file.seek(0)
                rv = make_response(package_file.read())
                rv.headers.set('Content-Type', 'application/zip')
                rv.headers.set(
                    'Content-Disposition', 'attachment', filename='local.zip')
                package_file.close()
                return rv
        except ClientError as e:
            # Handle S3 download error
            logging.error("get s3://%s/%s" % (self.bucket_name, key))
            logging.error(e)
            return "Record not found", 400
        pass

    def __init__(self, bucket_name, access_key=None, secret_key=None, session_token=None):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               aws_session_token=session_token)

    def get_metadatas(self, namespace, name, provider):
        """
        Search in an S3 different version of an package
        :param namespace: Namespace for package to search
        :param name: Name of package to search
        :param provider: Provider for package to search
        :return: Array with version
        """
        logging.debug(
            'Search package %s/%s/%s/*.desc.yml on s3 repository : %s' % (namespace, name, provider, self.bucket_name))
        objects = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix="%s/%s/%s/" % (namespace, name, provider)
        )
        logging.debug(json.dumps(objects, default=str))

        if objects['KeyCount'] < 1:
            return "Record not found", 400

        return_array = []
        # list file with name end by .desc.yml
        for obj in objects['Contents']:
            if obj['Key'].endswith('.desc.yml'):
                try:
                    # Download yml file and add content to response
                    with tempfile.TemporaryFile() as package_file:
                        self.s3.download_fileobj(self.bucket_name, obj['Key'], package_file)
                        package_file.seek(0)
                        file_as_string = package_file.read().decode('utf-8')
                        metadata = yaml.safe_load(file_as_string)
                        return_array.append(metadata)
                except ClientError as e:
                    # Handle S3 download error
                    logging.error(e)
                except ScannerError as e:
                    # Handle YML parsing error
                    logging.error(e)
        return return_array

import json
import logging
import tempfile

from botocore.exceptions import ClientError
from yaml.scanner import ScannerError

from api.PackageStorageBackends import PackageStorageBackend
import boto3
import re
import yaml



class S3StorageBackend(PackageStorageBackend):
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
        for obj in objects['Contents']:
            if obj['Key'].endswith('.desc.yml'):
                try:
                    with tempfile.TemporaryFile() as package_file:
                        self.s3.download_fileobj(self.bucket_name, obj['Key'], package_file)
                        package_file.seek(0)
                        file_as_string = package_file.read().decode('utf-8')
                        metadata = yaml.safe_load(file_as_string)
                        return_array.append(metadata)
                except ClientError as e:
                    logging.error(e)
                except ScannerError as e:
                    logging.error(e)
        return return_array

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 TfPrivateRegistry

 A Front API to distribute Terraform modules.
 Can be access via AWS API-Gateway and Lambda or standalone
"""

__author__ = 'Mathieu GOULIN'
__copyright__ = 'Copyright 2022, MGOULIN'
__credits__ = ['']
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = 'Mathieu GOULIN'
__email__ = 'mathieu.goulin@gadz.org'
__status__ = 'in progress'

#################################################
# Load Modules
#################################################
import os
from flask import Flask
from api.Middleware import Middleware
from api.AWS import S3StorageBackend

#################################################
# Fetch Env
#################################################
bucket_name = os.environ.get('BUCKET_NAME')
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
session_token = os.environ.get('AWS_SESSION_TOKEN')

#################################################
# Starting App
#################################################
app = Flask(__name__)
backend = S3StorageBackend(bucket_name, access_key=access_key, secret_key=secret_key, session_token=session_token)
m = Middleware(backend)


# Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return m.discovery()


# Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def get_versions(namespace, name, provider):
    return m.get_versions(namespace, name, provider)


# Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def download_version(namespace, name, provider, version):
    return m.x_header(namespace, name, provider, version)


# need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def download_file(namespace, name, provider, version):
    return m.download_file(namespace, name, provider, version)


app.run()
# EOF

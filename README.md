# TfPrivateRegistry!

This is an implementation of terraform registry api : https://www.terraform.io/registry/api-docs

# Usage

## Running daemon

````
export BUCKET_NAME=terraform_modules
export AWS_ACCESS_KEY_ID=1234567890  
export AWS_SECRET_ACCESS_KEY=abcdefghijklm
export AWS_SESSION_TOKEN=abcdefghijklm

python main.py
````
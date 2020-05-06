# coding:utf-8

import os
from flask import Flask, request, jsonify

import urllib.request
from google.cloud import storage


def handle(request):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }

        return ('', 204, headers)

    project_id = os.environ['PROJECT_ID']
    bucket_name = os.environ['BUCKET_NAME']
    url = os.environ['SOURCE_URL']
    destination_blob_name = os.environ['DEST_NAME']
    content_type = os.environ['CONTENT_TYPE']

    client = storage.Client()

    file = urllib.request.urlopen(url)

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file.read(), content_type=content_type)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
    }

    results = {'result': 'success'}

    return (jsonify(results), 200, headers)


if __name__ == '__main__':

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'OPTIONS'])
    def index():
        return handle(request)

    app.run()

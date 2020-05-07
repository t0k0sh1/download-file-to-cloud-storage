# coding:utf-8

import os
from flask import Flask, request, jsonify

import urllib.request
from google.cloud import storage


def handle(event, context):
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

    results = {'result': 'success'}

    return jsonify(results)

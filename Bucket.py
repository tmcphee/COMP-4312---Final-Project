
import os
import binascii
import collections
import datetime
import hashlib
import sys
import six

from google.oauth2 import service_account
from google.cloud import storage
from six.moves.urllib.parse import quote


def create_bk():
    try:
        storage_client = storage.Client()
        storage_client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
        bucket = storage_client.create_bucket(os.environ['BUCKET_NAME'])
        print("Bucket {} created".format(os.environ['BUCKET_NAME']))
        return True
    except Exception as e:
        print("Bucket name is either existing or invalid format -> ".format(e))
        return False


def upload_file(path, name):
    try:
        storage_client = storage.Client()
        storage_client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
        bucket = storage_client.bucket(os.environ['BUCKET_NAME'])

        blob = bucket.blob(path)
        blob.upload_from_filename(name)
        return True
    except Exception as e:
        print("Unable to upload file -> ".format(e))
        return False


def download_file(path, name):
    storage_client = storage.Client()
    storage_client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    bucket = storage_client.bucket(os.environ['BUCKET_NAME'])

    blob = bucket.blob(path)
    blob.download_to_filename(name)

'''
def get_signed_url():
    storage_client = storage.Client()
    storage_client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    bucket = storage_client.bucket(os.environ['BUCKET_NAME'])

    file = bucket.file()
'''


def list_files():
    blob_names = []
    storage_client = storage.Client()
    storage_client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    blobs = storage_client.list_blobs(os.environ['BUCKET_NAME'])

    for blob in blobs:
        blob_names.append(blob.name)

    return blob_names


def generate_signed_url(service_account_file, bucket_name, object_name,
                        subresource=None, expiration=604800, http_method='GET',
                        query_parameters=None, headers=None):

    if expiration > 604800:
        print('Expiration Time can\'t be longer than 604800 seconds (7 days).')
        sys.exit(1)

    escaped_object_name = quote(six.ensure_binary(object_name), safe=b'/~')
    canonical_uri = '/{}'.format(escaped_object_name)

    datetime_now = datetime.datetime.utcnow()
    request_timestamp = datetime_now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = datetime_now.strftime('%Y%m%d')

    google_credentials = service_account.Credentials.from_service_account_file(
        service_account_file)
    client_email = google_credentials.service_account_email
    credential_scope = '{}/auto/storage/goog4_request'.format(datestamp)
    credential = '{}/{}'.format(client_email, credential_scope)

    if headers is None:
        headers = dict()
    host = '{}.storage.googleapis.com'.format(bucket_name)
    headers['host'] = host

    canonical_headers = ''
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k, v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += '{}:{}\n'.format(lower_k, strip_v)

    signed_headers = ''
    for k, _ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += '{};'.format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'

    if query_parameters is None:
        query_parameters = dict()
    query_parameters['X-Goog-Algorithm'] = 'GOOG4-RSA-SHA256'
    query_parameters['X-Goog-Credential'] = credential
    query_parameters['X-Goog-Date'] = request_timestamp
    query_parameters['X-Goog-Expires'] = expiration
    query_parameters['X-Goog-SignedHeaders'] = signed_headers
    if subresource:
        query_parameters[subresource] = ''

    canonical_query_string = ''
    ordered_query_parameters = collections.OrderedDict(
        sorted(query_parameters.items()))
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe='')
        encoded_v = quote(str(v), safe='')
        canonical_query_string += '{}={}&'.format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing '&'

    canonical_request = '\n'.join([http_method,
                                   canonical_uri,
                                   canonical_query_string,
                                   canonical_headers,
                                   signed_headers,
                                   'UNSIGNED-PAYLOAD'])

    canonical_request_hash = hashlib.sha256(
        canonical_request.encode()).hexdigest()

    string_to_sign = '\n'.join(['GOOG4-RSA-SHA256',
                                request_timestamp,
                                credential_scope,
                                canonical_request_hash])

    # signer.sign() signs using RSA-SHA256 with PKCS1v15 padding
    signature = binascii.hexlify(
        google_credentials.signer.sign(string_to_sign)
    ).decode()

    scheme_and_host = '{}://{}'.format('https', host)
    signed_url = '{}{}?{}&x-goog-signature={}'.format(
        scheme_and_host, canonical_uri, canonical_query_string, signature)

    return signed_url


def get_signed_url_credfile(object_name):
    return generate_signed_url(
        service_account_file=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        http_method='GET', bucket_name=os.environ['BUCKET_NAME'],
        object_name=object_name, subresource=None,
        expiration=604800)


def web_list_blobs(host):
    liststr = ""
    for x in list_files():
        url = get_signed_url_credfile(x)
        liststr += "<a style=\"color:white\" download=\"text\" href=\"" + url + "\">"
        liststr += x
        liststr += "</a><br>"

    return liststr




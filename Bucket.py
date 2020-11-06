from google.cloud import storage
from storage_list_files import return_blobs
from storage_create_bucket import create_bucket
from storage_upload_file import upload_blob

bucket_name = "comp4312_a2_0670448"


def create_bk():
    try:
        create_bucket(bucket_name=bucket_name)
        print("Bucket {} created".format(bucket_name))
        return True
    except:
        print("Bucket name is either existing or invalid format")
        return False


def upload_file(path, name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(path)
    blob.upload_from_filename(name)


def download_file(path, name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(path)
    blob.download_to_filename(name)


def get_signed_url(path, name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    file = bucket.file()



def list_files():
    blob_names = []
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        blob_names.append(blob.name)

    return blob_names


def web_list_blobs():
    liststr = ""

    for x in list_files():
        liststr += "<form method=\"post\">"
        liststr += "<strong>" + x + "</strong>"
        liststr += "<button type=\"submit\" class=\"btn btn-danger\" name=\"Download\"value=" + x + ">Download</button>"
        liststr += "</form>"

    return liststr


def web_dl_blob():
    print("")
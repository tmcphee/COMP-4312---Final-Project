# Hotel Review Analyzer
#### COMP-4312 Final Project
The application uses a machine learning model to determine if a hotel review is positive or negative. The applicaion hosts a web interface where the user can pass a review to the trained model to be analyzed. 

The Hotel Review Analyzer uses python flask to host the web interface

### Features:
* Machine learning model to analyze and determine if a review is positive or negative.
* SQL to store new data
* Docker image for easy deployment

## Usage
`` docker run --name=Hotel-Review-Analyzer -d -p 8080:8080 -v /path/to/config:/config:rw  tmcphee/hotelreviews``

##### The Docker requires two files to be placed into a the mapped /config folder
> credentials.json 

The file can be downloaded [Here](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.200870509.238563060.1604591851-1077707084.1600187677)


> hotelreviews.conf
```
  {
  "instance_name": "PUT-SQL-INSTANCE-NAME-HERE",
  "bucket_name": "PUT-BUCKET-NAME-HERE"
  }
```

If running on windows the credentials.json and hotelreviews.conf should be placed into the root directory

### Configuration
##### Bucket Roles (Signed URL):
1. Open the Cloud Storage browser in the Google Cloud Console.
[Open Cloud Storage Browser](https://console.cloud.google.com/storage/browser?_ga=2.266979021.238563060.1604591851-1077707084.1600187677)
2. Click the Bucket overflow menu () associated with the bucket to which you want to grant a member a role.
3. Choose Edit bucket permissions.
4. Click the + Add members button.
5. In the New members field
> Member: BUCKET-NAME@PROJECT-NAME.iam.gserviceaccount.com
6. Select the role Storage Object Admin
7. Click Save.

### Links:
* [Docker](https://hub.docker.com/r/tmcphee/hotelreviews)
* [Dataset](https://www.kaggle.com/harmanpreet93/hotelreviews)

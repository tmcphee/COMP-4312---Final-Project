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

##### The application requires two files to be placed into a the mapped /config folder or in the root directory
> credentials.json 

The file can be downloaded [Here](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.200870509.238563060.1604591851-1077707084.1600187677)


> hotelreviews.conf
```
  {
  "instance_name": "PUT-SQL-INSTANCE-NAME-HERE",
  "bucket_name": "PUT-BUCKET-NAME-HERE",
  "SQL_HOST": "127.0.0.1",
  "SQL_USER": "root",
  "SQL_PASSWORD": "password",
  "SQL_DB": "hotel_reviews"
  }
```

###### Optonal:
The configuration can be defined using ENV Variables
```
  ENVIRONMENT: "Linux"
  HOST: "0.0.0.0"
  GOOGLE_APPLICATION_CREDENTIALS: "credentials.json"
  INSTANCE_NAME: "PUT-SQL-INSTANCE-NAME-HERE"
  BUCKET_NAME: "PUT-BUCKET-NAME-HERE"
  SQL_HOST: "127.0.0.1"
  SQL_USER: "root"
  SQL_PASSWORD: "comp4312admin"
  SQL_DB: "hotel_reviews"
```

###### Optonal:
Generate credentials.json from ENV variables
```
  GOOGLE_CRED_ENV: Create
  type VALUE-HERE
  project_id VALUE-HERE
  private_key_id VALUE-HERE
  private_key VALUE-HERE
  client_email VALUE-HERE
  client_id VALUE-HERE
  auth_uri VALUE-HERE
  token_uri VALUE-HERE
  auth_provider_x509_cert_url VALUE-HERE
  client_x509_cert_url VALUE-HERE
```

If the host is `0.0.0.0` then the system assumes the service is running via Linux. 
If the host is `127.0.0.1` then the system assumes the service is running via Windows

This is important to note as the system will use the appropriate SQL_Proxy accordingly 

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

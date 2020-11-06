# set base image (host OS)
FROM python:3.8

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install wget -y

RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
RUN chmod +x cloud_sql_proxy

# copy the content of the local src directory to the working directory
COPY . .

RUN unzip -f /Dataset/LR.zip -d /Dataset

# command to run on container start
CMD [ "python", "main.py", "0.0.0.0" ]

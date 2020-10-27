cd /D "%~dp0"
docker run python:3.8
docker build -t hotelreview .
docker run -d -p 8080:8080 hotelreview
docker ps

start "" http://127.0.0.1:8080

pause
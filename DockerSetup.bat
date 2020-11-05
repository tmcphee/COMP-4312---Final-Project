cd /D "%~dp0"

docker build -t hotelreview .
docker tag hotelreview tmcphee/hotelreview

docker run -d -p 8080:8080 hotelreview
docker ps

start "" http://127.0.0.1:8080

pause
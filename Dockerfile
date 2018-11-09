FROM ubuntu:latest
RUN apt-get update -y 
RUN apt-get install -y python-pip python-dev build-essential 
RUN apt-get install -y libsm6 libxext6 libfontconfig1 libxrender1
ENV HTTP_PROXY http://10.74.1.1:8080
COPY . /app 
WORKDIR /app
RUN pip install --proxy=${HTTP_PROXY} -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
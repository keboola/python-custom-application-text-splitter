FROM quay.io/keboola/docker-custom-python:latest

RUN pip install pytest-cov
COPY . /code/
WORKDIR /data/
CMD ["python", "-u", "/code/main.py"]

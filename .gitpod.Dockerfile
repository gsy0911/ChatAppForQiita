FROM python:3.7
RUN pip install pipenv
RUN apt-get update
RUN apt-get install -y jq

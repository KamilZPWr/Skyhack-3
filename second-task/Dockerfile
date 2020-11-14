FROM python:3.7 as base

RUN mkdir /service
WORKDIR /service

RUN apt-get update && apt-get -y install git
RUN apt-get update && apt-get -y install ffmpeg


FROM base

COPY service /service/service
COPY models /service/models

COPY ./run.sh /service
COPY requirements.txt /service
COPY run_app.py /service
COPY setup.py /service

RUN mkdir -p storage

RUN touch storage/jobs.json
RUN echo {} > storage/jobs.json

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD [ "bash", "run.sh" ]

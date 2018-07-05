FROM python:3.5

RUN mkdir /code
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["entrypoint.sh"]

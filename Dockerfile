FROM python:3
ENV  BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAPYSVwEAAAAAOpAjc1LhwtsistR3%2Bta0%2FAMw3N4%3D1oTAtsKNkPEUakbi9xTznam4DBrjlZrEpqyMDNoO4fg68K8YaE'

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
ADD . /code/
ENTRYPOINT [ "python3" ]
CMD ["server.py"]

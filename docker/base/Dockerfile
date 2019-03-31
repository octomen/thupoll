FROM python:3

USER 1000

COPY requirements/common.txt common_requirements.txt
RUN pip install --no-cache -r common_requirements.txt

ENV PYTHONPATH=/app
ENV FLASK_APP=thupoll.app_factory:init_app

WORKDIR /$PYTHONPATH

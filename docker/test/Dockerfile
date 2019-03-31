FROM octoman/base

COPY requirements/test.txt test_requirements.txt
RUN pip install --no-cache -r test_requirements.txt

COPY migrations $PYTHONPATH/migrations
COPY entrypoint.sh $PYTHONPATH/entrypoint.sh
COPY scripts $PYTHONPATH/scripts
COPY thupoll $PYTHONPATH/thupoll
COPY tests $PYTHONPATH/tests

USER 1000

CMD [ "./entrypoint.sh" ]

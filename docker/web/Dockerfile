FROM octoman/base

COPY migrations $PYTHONPATH/migrations
COPY entrypoint.sh $PYTHONPATH/entrypoint.sh
COPY scripts $PYTHONPATH/scripts
COPY thupoll $PYTHONPATH/thupoll

CMD [ "./entrypoint.sh" ]

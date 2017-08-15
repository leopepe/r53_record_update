FROM iron/python:3

RUN mkdir /app
COPY ./r53_record_update /app/r53_record_update
COPY ./packages /app/packages
ENV PYTHONPATH /app/packages
WORKDIR /app
ENTRYPOINT ["python3", "-m", "r53_record_update"]
CMD [""]
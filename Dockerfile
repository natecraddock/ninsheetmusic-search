FROM alpine:3.17

EXPOSE 8080

RUN apk add --no-cache python3 tzdata
RUN python3 -m ensurepip

RUN mkdir app/

RUN addgroup -S flask && adduser -S flask -G flask
RUN chown flask:flask app/
USER flask

COPY setup.py app/
COPY sheetmusic/ app/sheetmusic/

WORKDIR app/
RUN pip3 install .

CMD ["python3", "-m", "waitress", "--port", "8080", "--call", "sheetmusic:create_app"]

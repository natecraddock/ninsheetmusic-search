# ninsheetmusic-search

I was tired of the click-only navigation on the official [ninsheetmusic.org](ninsheetmusic.org)
so I made this simple Flask app. This is intended to be self-hosted. It requires very little resources,
and is very small and requires no front-end JavaScript.

## Deploying

I don't have builds hosted anywhere. Clone the repo, then run the following commands to get started.

```
$ docker build --tag ninsheetmusic:latest .
```

Run server

```
$ docker run -d -p 8080:8080 --restart unless-stopped --name ninsheetmusic ninsheetmusic:latest
```

The server will now be available at localhost:8080 (or whatever port you exposed)

Populate database

```
$ docker exec ninsheetmusic python3 -m flask --app sheetmusic init-db
```

* healthcheck
* db in separate volume

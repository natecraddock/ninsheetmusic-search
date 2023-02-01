DROP TABLE IF EXISTS metadata;
DROP TABLE IF EXISTS music;

CREATE TABLE metadata (
    last_update TIMESTAMP,
    num_sheets INTEGER NOT NULL
);

CREATE TABLE music (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    title_plain TEXT NOT NULL,
    game TEXT NOT NULL,
    game_plain TEXT NOT NULL,
    series TEXT NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL
);

CREATE INDEX music_idx on music (title, game, series)

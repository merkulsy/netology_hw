-- 1. Жанры
CREATE TABLE IF NOT EXISTS genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Исполнители
CREATE TABLE IF NOT EXISTS artist (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE
);

-- 3. Связь исполнители - жанры (многие ко многим)
CREATE TABLE IF NOT EXISTS artist_genre (
    artist_id INTEGER NOT NULL REFERENCES artist(artist_id),
    genre_id INTEGER NOT NULL REFERENCES genre(genre_id),
    CONSTRAINT pk_artist_genge PRIMARY KEY (artist_id, genre_id)
);

-- 4. Альбомы (без привязки к одному исполнителю)
CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900 AND release_year <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- 5. Связь исполнители - альбомы (многие ко многим)
CREATE TABLE IF NOT EXISTS artist_album (
    artist_id INTEGER NOT NULL REFERENCES artist(artist_id),
    album_id INTEGER NOT NULL REFERENCES album(album_id),
    CONSTRAINT pk_artist_album PRIMARY KEY (artist_id, album_id)
);

-- 6. Треки (принадлежат одному альбому)
CREATE TABLE IF NOT EXISTS track (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration > 0),
    album_id INTEGER NOT NULL REFERENCES album(album_id)
);

-- 7. Сборники
CREATE TABLE IF NOT EXISTS collection (
    collection_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900 AND release_year <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- 8. Связь сборники - треки (многие ко многим)
CREATE TABLE IF NOT EXISTS collection_track (
    collection_id INTEGER NOT NULL REFERENCES collection(collection_id),
    track_id INTEGER NOT NULL REFERENCES track(track_id),
    CONSTRAINT pk_track_collection PRIMARY KEY (collection_id, track_id)
);
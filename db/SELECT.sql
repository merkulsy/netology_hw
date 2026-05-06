--Задание 2

-- 1. Название и продолжительность самого длительного трека
SELECT title AS track_title, duration AS duration_seconds
FROM track
WHERE duration = (SELECT MAX(duration) FROM track);

--2. Название треков, продолжительность которых не менее 3,5 минут
SELECT title AS track_title, duration AS duration_seconds
FROM track
WHERE duration >= 210
ORDER BY duration DESC;

--3. Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT title AS collection_title, release_year
FROM collection
WHERE release_year BETWEEN 2018 AND 2020
ORDER BY release_year;

--4. Исполнители, чьё имя состоит из одного слова
SELECT name AS artist_name
FROM artist
WHERE name NOT LIKE '% %';

--5. Название треков, которые содержат слово «мой» или «my».

-- Добавляем треки, которые ДОЛЖНЫ попасть в выборку
INSERT INTO track (title, duration, album_id) VALUES
('my own', 180, 4),
('own my', 180, 4),
('my', 180, 4),
('oh my god', 180, 4);

-- Добавляем треки, которые НЕ ДОЛЖНЫ попасть в выборку
INSERT INTO track (title, duration, album_id) VALUES
('myself', 180, 4),
('by myself', 180, 4),
('bemy self', 180, 4),
('myself by', 180, 4),
('by myself by', 180, 4),
('beemy', 180, 4),
('premyne', 180, 4);

SELECT title AS track_title
FROM track
WHERE 
   -- Для 'my'
   title ILIKE 'my' 
   OR title ILIKE 'my %' 
   OR title ILIKE '% my' 
   OR title ILIKE '% my %'
   -- Для 'мой'
   OR title ILIKE 'мой' 
   OR title ILIKE 'мой %' 
   OR title ILIKE '% мой' 
   OR title ILIKE '% мой %';



--Задание 3

--1. Количество исполнителей в каждом жанре
SELECT g.name AS genre_name, COUNT(ag.artist_id) AS artist_count
FROM genre g
LEFT JOIN artist_genre ag ON g.genre_id = ag.genre_id
GROUP BY g.genre_id, g.name
ORDER BY artist_count DESC;

--2. Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(t.track_id) AS track_count
FROM track t
JOIN album a ON t.album_id = a.album_id
WHERE a.release_year BETWEEN 2019 AND 2020;

--3. Средняя продолжительность треков по каждому альбому
SELECT a.title AS album_title, 
       AVG(t.duration) AS avg_duration_seconds,
       ROUND(AVG(t.duration) / 60, 2) AS avg_duration_minutes
FROM album a
LEFT JOIN track t ON a.album_id = t.album_id
GROUP BY a.album_id, a.title
ORDER BY avg_duration_seconds DESC;

--4. Все исполнители, которые не выпустили альбомы в 2020 году
SELECT DISTINCT ar.name AS artist_name
FROM artist ar
WHERE ar.artist_id NOT IN (
    SELECT aa.artist_id
    FROM artist_album aa
    JOIN album a ON aa.album_id = a.album_id
    WHERE a.release_year = 2020
);

--5. Названия сборников, в которых присутствует конкретный исполнитель (Imagine Dragons)
SELECT DISTINCT c.title AS collection_title, c.release_year
FROM collection c
JOIN collection_track ct ON c.collection_id = ct.collection_id
JOIN track t ON ct.track_id = t.track_id
JOIN album a ON t.album_id = a.album_id
JOIN artist_album aa ON a.album_id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'Imagine Dragons'
ORDER BY c.release_year;


--Задание 4

--Дополнительные данные
-- Добавляем альбом с 1 треком
INSERT INTO album (title, release_year) VALUES ('Single', 2024);
INSERT INTO track (title, duration, album_id) VALUES ('Only Track', 200, 5);
-- Связываем с исполнителем Moby
INSERT INTO artist_album (artist_id, album_id) VALUES (5, 5);


-- 1. Альбомы с исполнителями более одного жанра
SELECT DISTINCT a.title AS album_title
FROM album a
JOIN artist_album aa ON a.album_id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.artist_id
JOIN artist_genre ag ON ar.artist_id = ag.artist_id
GROUP BY a.album_id, a.title, ar.artist_id
HAVING COUNT(ag.genre_id) > 1;

-- 2. Треки не в сборниках
SELECT t.title AS track_title
FROM track t
LEFT JOIN collection_track ct ON t.track_id = ct.track_id
WHERE ct.track_id IS NULL;

-- 3. Исполнители самого короткого трека
SELECT ar.name AS artist_name, t.title AS track_title, t.duration
FROM track t
JOIN album a ON t.album_id = a.album_id
JOIN artist_album aa ON a.album_id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.artist_id
WHERE t.duration = (SELECT MIN(duration) FROM track);

-- 4. Альбомы с наименьшим количеством треков
SELECT title AS album_title, track_count
FROM (
    SELECT a.album_id, a.title, COUNT(t.track_id) AS track_count
    FROM album a
    LEFT JOIN track t ON a.album_id = t.album_id
    GROUP BY a.album_id, a.title
) track_counts
ORDER by track_count
LIMIT 1;  
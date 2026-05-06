--Задание 1
--Заполните БД, в ней должно быть:
--не менее 4 исполнителей,
--не менее 3 жанров,
--не менее 3 альбомов,
--не менее 6 треков,
--не менее 4 сборников.
--Внимание: должны быть заполнены все поля каждой таблицы, 
--в том числе таблицы связей исполнителей с жанрами, исполнителей с альбомами, сборников с треками.



-- 1. Заполнение жанров 
INSERT INTO genre (name) VALUES
('Рок'),
('Поп'),
('Электронная музыка'),
('Джаз');  


-- 2. Заполнение исполнителей 
INSERT INTO artist (name) VALUES
('Imagine Dragons'),
('Dua Lipa'),
('Daft Punk'),
('Norah Jones'),
('Moby');


-- 3. Связь исполнителей с жанрами 
INSERT INTO artist_genre (artist_id, genre_id) VALUES
(1, 1), (1, 3), -- Imagine Dragons: Рок + Электронная
(2, 2), (2, 3), -- Dua Lipa: Поп + Электронная
(3, 3), -- Daft Punk: Электронная
(4, 4), (4, 2), -- Norah Jones: Джаз + Поп
(5, 3); -- Moby: Электронная


-- 4. Заполнение альбомов 
INSERT INTO album (title, release_year) VALUES
('Night Visions', 2012),
('Future Nostalgia', 2020),
('Random Access Memories', 2013),
('Come Away with Me', 2002);


-- 5. Связь исполнителей с альбомами 
INSERT INTO artist_album (artist_id, album_id) VALUES
(1, 1),  -- Imagine Dragons -> Night Visions
(2, 2),  -- Dua Lipa -> Future Nostalgia
(3, 3),  -- Daft Punk -> Random Access Memories
(4, 4);  -- Norah Jones -> Come Away with Me


-- 6. Заполнение треков 
INSERT INTO track (title, duration, album_id) VALUES
('Radioactive', 186, 1), -- Night Visions
('Demons', 177, 1), -- Night Visions
('Levitating', 203, 2), -- Future Nostalgia
('Don''t Start Now', 183, 2), -- Future Nostalgia
('Get Lucky', 248, 3), -- Random Access Memories
('Instant Crush', 337, 3), -- Random Access Memories 
('Don''t Know Why', 186, 4), -- Come Away with Me
('My Heart Will Go On', 267, 4); -- дополнительный трек для условия 'my'


-- 7. Заполнение сборников 
INSERT INTO collection (title, release_year) VALUES
('Top Hits 2010s', 2020),   
('Electronic Vibes', 2021),
('Chill & Relax', 2022),
('Workout Beats', 2023),
('Best of Pop', 2023);


-- 8. Связь сборников с треками 
INSERT INTO collection_track (collection_id, track_id) VALUES
(1, 1), (1, 2), (1, 5), -- Top Hits 2010s (2020)
(2, 1), (2, 5), (2, 6), -- Electronic Vibes (2021)
(3, 2), (3, 7), -- Chill & Relax (2022)
(4, 1), (4, 3), (4, 4), -- Workout Beats (2023)
(5, 3), (5, 4), (5, 5); -- Best of Pop (2023)
Для запуска контейнера с первым заданием ```sudo docker-compose up --build```




если прям в лоб то что то аля ```UPDATE full_name
SET status = (
  SELECT status FROM short_name
  WHERE short_name.name_short = SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1)
)
WHERE EXISTS (
  SELECT 1 FROM short_name
  WHERE short_name.name_short = SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1)
)```

Но это будет долго, потому что подзапрос в каждой строке.
Можно попробовать сделать индексы аля
```CREATE INDEX idx_short_name_name ON short_name (name);
CREATE INDEX idx_full_name_name ON full_name (name);```

И запрос потом
```UPDATE full_name
JOIN short_name ON short_name.name = SUBSTR(full_name.name, 1, LENGTH(full_name.name) - LENGTH(SUBSTRING_INDEX(full_name.name, '.', -1)) - 1)
SET full_name.status = short_name.status;```

 либо что то аля 
```UPDATE full_name
LEFT JOIN short_name
ON SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) = short_name.name_short
SET full_name.status = IFNULL(short_name.status, 'unknown');```

можно попробовать использовать представления ```CREATE VIEW full_name_with_status AS
SELECT full_name.*, IFNULL(short_name.status, 'unknown') AS status
FROM full_name
LEFT JOIN short_name
ON SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) = short_name.name_short;```
 и потом 
```UPDATE full_name
SET status = (SELECT status FROM full_name_with_status WHERE full_name.id = full_name_with_status.id);```

можно временную таблциу создать ```
CREATE TEMPORARY TABLE temp_name_status AS
SELECT SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) AS name,
       short_name.status
FROM full_name
LEFT JOIN short_name
ON SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) = short_name.name_short;```
и потом ```UPDATE full_name
SET status = (SELECT status FROM temp_name_status WHERE SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) = temp_name_status.name);```

можно и подзапроосом ```UPDATE full_name
SET status = (SELECT IFNULL(short_name.status, 'unknown')
              FROM short_name
              WHERE SUBSTR(full_name.name_full, 1, LENGTH(full_name.name_full) - LENGTH(SUBSTRING_INDEX(full_name.name_full, '.', -1)) - 1) = short_name.name_short);``` 
но тут скорее всего будут проблемы с производительностью

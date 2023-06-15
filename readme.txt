Для запуска контейнера с первым заданием ```sudo docker-compose up --build```



Вариантов масса, от представлений до тригеров, функций и индексов -- см ниже.

```UPDATE full_names fn
SET status = (
  SELECT status
  FROM short_names sn
  WHERE sn.name = fn.name
)
WHERE name IN (SELECT name FROM short_names);```



```CREATE TEMP TABLE temp_short_names AS
SELECT name, status
FROM short_names;

UPDATE full_names fn
SET status = t.status
FROM temp_short_names t
WHERE fn.name = t.name;```




```COPY temp_short_names TO '/tmp/short_names.csv' WITH CSV;

COPY full_names (name, status)
FROM '/tmp/short_names.csv' WITH CSV;
```


```UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE fn.name = sn.name;```


```CREATE TRIGGER update_full_names_status
AFTER INSERT OR UPDATE ON short_names
FOR EACH ROW
EXECUTE PROCEDURE update_full_names_status();

CREATE OR REPLACE FUNCTION update_full_names_status()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE full_names
  SET status = NEW.status
  WHERE name = NEW.name;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;```



```CREATE MATERIALIZED VIEW short_names_with_status AS
SELECT name, status
FROM short_names;

UPDATE full_names fn
SET status = sn.status
FROM short_names_with_status sn
WHERE fn.name = sn.name;```



```CREATE OR REPLACE FUNCTION update_full_names_status()
RETURNS void AS $$
BEGIN
  UPDATE full_names fn
  SET status = sn.status
  FROM short_names sn
  WHERE fn.name = sn.name;
END;
$$ LANGUAGE plpgsql;
```


```CREATE INDEX short_names_name_idx ON short_names (name);
CREATE INDEX full_names_name_idx ON full_names (name);

UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE fn.name = sn.name;
```

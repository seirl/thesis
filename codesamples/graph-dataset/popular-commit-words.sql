-- Fist word of 1.1 billion commit messages ordered by decreasing frequency
-- (Run time: 29.79 seconds, Data scanned: 37.51 GB)
SELECT COUNT(*) AS c, word
FROM
  (SELECT LOWER(REGEXP_EXTRACT(FROM_UTF8(
          message), '^\w+')) AS word
  FROM revision )
WHERE word != ''
GROUP BY  word
ORDER BY  COUNT(*) DESC LIMIT 20;

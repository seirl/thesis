-- Most popular file name (in terms of number of different versions)
--  (Run time: 3 minutes 40 seconds, Data scanned: 150.68 GB)
-- cnt 182,373,697
SELECT FROM_UTF8(name, '?') AS name,
  COUNT(DISTINCT target) AS cnt
FROM directory_entry_file
GROUP BY name
ORDER BY cnt DESC
LIMIT 1;

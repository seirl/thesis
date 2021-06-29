-- Most popular snapshots by visit count
SELECT
  'https://archive.softwareheritage.org/browse/snapshot/' || lower(to_hex(snapshot.id)),
  count(*) AS popularity
FROM origin_visit
INNER JOIN snapshot ON snapshot.object_id = snapshot_id
WHERE snapshot_id IS NOT NULL
GROUP BY snapshot.id
ORDER BY popularity DESC
LIMIT 100;

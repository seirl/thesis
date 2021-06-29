-- Average fork size of revisions
-- (Run time: 21.77 seconds, Data scanned: 23.33 GB)
-- Result is 1.0881200349675373
SELECT AVG(fork_size)
FROM (SELECT COUNT(*) AS fork_size
        FROM revision_history
        GROUP BY  parent_id);

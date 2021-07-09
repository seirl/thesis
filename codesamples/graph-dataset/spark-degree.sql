%sql
select degree, count(*) from (
  select source, count(*) as degree from (
    select hex(source) as source,
           hex(target) as dest from (
      select id as source,
             explode(dir_entries) as dir_entry
      from directory)
    inner join directory_entry_file
      on directory_entry_file.id = dir_entry
  )
  group by source
)
group by degree
order by degree

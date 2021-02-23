# SWH

- software heritage goals
    - archival
    - research platform
        - more emphasis on research goals
- how software heritage works (listing / loading)
- project goal: trying to be as exhaustive as possible, no filtering of
  "important" code, binaries etc
- the software heritage data model
    - uniform
    - deduplicated
        - data sharing
- high deduplication and combinatorial explosion
    - duplication coming from development practices of copying / forking
    - ESE article (zack+grouss)
- exponential growth
    - ESE article (zack+grouss) + OSS gender differences (zack)
- mirroring: swh-journal


# Large scale analysis

- we want to make analysis of all the data *stored in SWH* possible
    - (we can't track issues, etc.)

- collection of use cases
    - list of MSR articles with categorized use cases
    - no need to be exhaustive, give examples
    - give limitations of past studies (small datasets, things that were
      impossible before SWH)

- *phases* of analyses
    - selecting the data of interest
    - analysing it

- *kinds* of data available in the Software Heritage archive
    - content
    - filtering on metadata
    - full-text search on contents
    - history graph
    - derived graph data
        - provenance indexing: derived provenance graph
        - diff graph data
        - community graph
        - dependencies

- prototyping: subdatasets

- (to be placed): how to do all of this in a scalable way?


# Making the data available

## vault

- Base naive solution, fetch a single artifact
- Directory/revision/snapshot cookers
    - git fast-import, computing diff trees
- pro/con: Losing the deduplication aspect when doing analysis, can be used
  with any standard analysis tool

## swh-fuse

- Mounting the archive locally
- Great for prototyping, analysis tools usable directly on the code after a
  mount

## blobs

Put everything in a public S3 bucket, indexed by hash -> already scalable
    - TODO: Tool to retrieve them all

- Monolithic data, you never select *on* blobs outside code search, you
  just access the ones you need to perform your analysis.
  Boolean download/don't download

- Attempts at packing/deduplication
    - Rolling hashes (+benchmarks)
    - git/pack-heuristics to cite / future work

## property graph dataset

- The SWH graph dataset: all the metadata that contains the filesystem,
  history and hosting layers.

- Graph representation vs relational representation
    - static columnar format: ORC/Parquet
    - Edges format

- Privacy: anonymization
    - Georgios / GHTorrent had a problem with that, possibly cite

- Denormalization: why is it hard to denormalize graphs?
    - "flat" mappings would take huge amounts of space
    - woc does it, but they remove "annoying" data. we want fidelity.

## Export from our database

- Attempt: S3 object exporter, working on hash ranges
    - non-incremental

- Attempt: from already relational data
    - requires impractical joins for denormalization
    - Mix of hive/redshift/awk/...

- swh-dataset/swh-journal contributions
    - parallelization logic
    - avoiding dangling objects
    - sqlite / kyotocabinet / ... for node unicity
    - sort for destination nodes

## Analysis platforms

- Cloud engines / Hadoop local cluster
    - Athena, Redshift, Databricks, BigQuery
    - Utilities to upload automatically the table schemas

- Very fast scalable queries for everything that is *local*
    - Examples of local queries: in degree, out degree, diomidis' queries

- Limitations
    - Athena/prestodb joins
        - automatic scale out vs manual cluster management
    - normalized directory arrays
        - scale factor impossible to estimate => timeouts
        - bigquery row limit
        - we have to denormalize to run queries on directories
    - recursive queries impossible -- limited to one single layer


# Working with graph representation

## Challenges

- relational data is a graph, intrinsically not flat.

- lots of linked and interdependant data, not a flat representation like for
  contents
- simply partitioning by hash like for contents or doing sequential scans isn't
  satisfactory
    - you don't have a list of graph nodes from the start, you need to
      discover them
    - you need graph algorithms!

- Neo4J/AIGraph don't scale to our size
    - cite constraints

## NetworkX

- Graph queries with NetworkX
- Extremely expensive
- Pretty slow (especially if you multiply by the number of machines)
- Requires implementation of parallel graph algorithms

## Graph compression

### Why?

- Fit the graph in memory of a single machine
- Run standard graph algorithm without particular work on making them parallel
- Great for prototyping
- Analyzing the structure of the graph unlocks sharding feasability studies

### Compressing the graph

- SANER paper
- benchmarks
- LLP compression
- memory sharing with cachemount in /dev/shm

Explain the tradeoffs: what to put in memory
    - let the user choose what they want to mmap in memory/ssd/hdd depending on
      constraints

## Graph metadata

Node metadata:
    - SWHIDs: mappings, signed MPH
    - types: in memory bit vector
    - all the rest: depends on the type of metadata
        - timestamp: array of longs
        - commit messages: frontcodedstringlist

Edge metadata:
    - Label compression pipeline
    - MPH benchmarks -> monotone pick
    - reverse mapping benchmarks

## Subdatasets

- % of origins you need for % of the archive
- label slicing, node metadata slicing
- ImmutableSubgraph
- lazy Subgraphs
- popular3kpython / popular4k
    - find the object ids using swh-graph, then join them in athena to get the
      relational format

## High level query API

- Python <-> Java gateway
    - py4j vs jni considerations
- Simple query API: RPC
    - Traversal queries, visit/leaves/... + count
    - Limits and filtering

- Expressivity
    - examples of data queries that cannot be made using this simple language
    - mixed solution java impl / http queries
    - exploration of graph query languages

# The structure of the graph

Understanding the structure of the graph is important to know how to
shard/analyze it more efficiently

## Low level properties

Topology paper:

- In/out degrees
- Connected components
- Clustering distribution
- Average path
- Multiplication coefficient (SANER benchmark)

## Structure of projects and forks
(Have that in applications?)

Forks paper


# Applications

## Derived metadata

- Paper with kevin

## Scheduling predictions (NOT DONE)

- Look at timestamps of commits to know which project should be scheduled when

## Sharding (NOT DONE)

- Projects are relatively neatly separable using fork cliques until the
  revision layer
- Remove nodes by indegree: doesn't work, still huge component
- Remove nodes by pagerank: ???

=> We can't split the graph neatly using connected components on the entire
graph. We have to do a best-effort sharding that minimizes roundtrips

Evaluation of how well we can do that using different sharding methods:
- BFS order
- Fork cliques (duplication size?)
- connected components at the revision level (duplication size?)

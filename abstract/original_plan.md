# Enabling Big Code analysis on a very large source code corpus

## Context

Software Heritage is an ambitious digital preservation initiative that is
amassing unprecedented amounts of software source code from a variety of
origins, and keeps track of all their evolution history, as captured by version
control systems. This is leading to the creation of one of the largest source
code corpus and is building the corresponding development graph where the nodes
are the contents of the source files, directories and commit points, and the
edges carry the name of the files, and the links between commits and
directories.

The availability of this universal software source code knowledge base provides
unique opportunities for what is now known as “Big Code” research: querying,
analysing and extracting knowledge both from the contents of the data and from
the structure of the commit graph. We expect that having a way to leverage the
data contained in very large source code archives that include development
history, like the Software Heritage archive, will pave the way to learn more
about the evolution of software at a very large scale than it has ever been
possible before.

The exploitation of such an unprecedented very large source code collection
poses significant challenges in terms of data representation, query languages,
system architecture and specialised algorithms.

# Objectives of the thesis

The main focus of the thesis will be to find efficient ways to perform large
scale computations not only on the content of the archive, but also on useful
data that could be derived from it, like code diffs, releases, branch/merge
history, and reuse patterns.

The current data representation structure of Software Heritage is a Merkle DAG,
which allows efficient deduplication, verification, and indexing of the content
of the archive. While this format is cost-efficient for preservation purposes,
it has not been designed with large scale analysis in mind. The current design
uses data indirections extensively, which adds considerable latency to
read-intensive operations. An important part of our goal will be to explore
more efficient ways of storing and indexing all the software artifacts
currently contained in the DAG, to allow for intensive computations to take
place on the archive.

As part of this quest for the most efficient data representation for such an
archive, we will look for heuristics to find and isolate repetitive code
snippets, as it would not only allow to deduplicate and analyze the content at
a more fine-grained level, but also give valuable insights to implement
efficient storage, retrieval, and analysis of those snippets.

Another important aspect that will be looked into is the interface for
performing computations on the archive. As the Merkle DAG structure is pretty
unique, we will investigate ways of performing efficient and expressive queries
by working on a query language that operates on this structure. This language
could either be an adaptation or an extension of relational algebra
implementations like SQL, or a completely new domain-specific language.

As we expect this project to become an important gateway for scientists working
on Big Code analysis, the thesis will have to work with efficient distributed
architectures as an integral part of the project’s design. For instance, it
should be easy and cost-efficient to make the analysis infrastructure scale-out
to accommodate for load increases. At the same time, the deployment should be
easy, for example allowing instantiation on state-of-the-art public cloud
offering.

Finally, the thesis will necessarily include practical applications and
experimental validation of the analysis approach, in order to show meaningful
results and usage examples, and as a way to test the general usability of the
system.

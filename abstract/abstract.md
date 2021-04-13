# Organizing the graph of public software development for ultra-large-scale mining

## Context

Software Heritage is an ambitious digital preservation initiative that is
amassing unprecedented amounts of software source code from a variety of
origins, and keeps track of all their evolution history, as captured by version
control systems (VCS). The Software Heritage archive has grown to be the
largest and most comprehensive corpus of public software artifacts,
encompassing all the major source code hosts (e.g. GitHub, Gitlab, Bitbucket,
Google Code) and supporting a variety of VCS (e.g. Git, Mercurial, SVN) and
package managers (Debian, NixOS, PyPI, NPM...).

This data is stored in a canonical format and deduplicated across the entire
archive at the level of software artifacts, which constructs a giant shared
graph of software development, where the nodes are the source files,
directories and commits, and the edges carry the names of the files and the
links between commits and directories.

The availability of this universal software development knowledge base provides
unique opportunities for what is now known as “Big Code” research: querying,
analysing and extracting knowledge both from the contents of the data and from
the structure of the development history graph. Making this data accessible to
researchers could unlock new capabilities in the software mining field. Being
able to run experiments on the entire graph of public software development
could help us gain an deeper understanding of the evolution of software at a
macro level, and the underlying social structures that compose it. It would
also reduce the barriers of entry to empirical studies by lowering the costs of
data collection and eliminating the need for manual data scraping and
retrieval, as well as facilitate replicating studies at larger scales using
comprehensive data samples.

The exploitation of such an unprecedented source code collection poses
significant challenges in terms of availability, data representation, system
architecture and scalability. The giant graph in the Software Heritage archive
contains more than 20 billion nodes and 200 billion edges, growing faster every
day. At this scale, few off-the-shelf tools can be used for general purpose
data analysis, and new techniques must be built on the state of the art of
large graph processing.

# Data availability

To better understand the kinds of data that need to be made available, we
systematically categorize the functional requirements of researchers in
software mining studies.  We classify the data available in the Software
Heritage archive, including the content of the source code files, the
development history and other kinds of metadata, but also data that can be
derived from the graph: commit diffs, dependency graphs, community graphs, etc.

Our first step towards providing a general purpose platform for data analysis
is to make the data available in a crude but still exploitable format. As this
can gather interest towards using the archive for research purposes, it
allows us to better understand the challenges of exploiting it, by identifying
the main pain points of researchers and limitations of the different formats.

We provide a few utilities to fetch the data at a micro-level: the vault, a
simple tool to gather the transitive closure of a specific software artifact in
the graph and then representing it in an open format; SwhFS, a virtual
filesystem to run common programs on the code stored in the archive without
having to pre-download it; and finally a simple way to download a list of
source code files from a cloud storage service.

To make possible macro analyses on the entire graph, we extract from the
archive a property graph containing all the software development metadata at
the filesystem, history and hosting levels. We represent it in two different
relational formats: a columnar format for scalable cloud processing, and a
format suitable for import in local databases for in-house analysis. We discuss
various considerations related to the dataset: the different formats,
performance, data denormalization and data privacy.
Putting these datasets on cloud platforms allows us to understand the use cases
for which this relational format is suitable, as well as its limitations,
notably the difficulty of running experiments that require graph traversal
algorithms (e.g walking down a commit chain).

# Graph representation

As the graph dataset is an inherently recursive structure, big data analysis
tools that exploit the "flatness" of data to scale-out their processing cannot
be used in a similar fashion on problems that are not embarrassingly parallel.
A naive scale-out approach to randomly assign the artifacts to different shards
is not very efficient, as a traversal algorithm will require jumping
between different shards all the time. We investigate existing scale-out
solutions (GraphFrames, Neo4J, AIGraph) and discuss their limitations for
scale-out graph analysis.

Another approach is that of graph compression: using existing techniques for
compressing very large graphs, we can fit the topology of the Software Heritage
graph in memory on a single machine. This allows us to run standard graph
algorithms without having to find a way to parallelize them. The compressed
graph can be used for prototyping purposes, but also as a production service
that can answer simple traversal queries. The thesis discusses the different
compression techniques used to fit the entire graph topology in only ~150 GB,
as well as some storage trade-offs for the node and edge metadata on the
property graph.

To let researchers run experiments on a smaller scale, we introduce a way to
extract representative graph subdatasets of any given size from the archive. We
discuss various implementations of ways to obtain a "view" of a given part of
the archive, and make some "teaser" datasets available using these techniques.

# Graph structure

Understanding the structure of the development graph is a fundamental step
towards scale-out analysis, as it can help us determine how to partition the
data into tightly knit clusters. Moreover, getting a better sense of the
topology of its different layers as well as their edge cases will help us
better organize the data for some domain-specific algorithms.

As a first step, we look at the low-level topological properties of the graph,
by systematically measuring a few key metrics on its different layers:
in-degree and out-degree distributions, connected component sizes, clustering
coefficients, average path lengths. We compare these metrics with other
large-scale graphs generated by human activities (social networks, graph of the
Web, ...).

On a macro-level, we seek to understand how the software artifacts are
organized and shared across different repositories by studying the notion of
"forks" in the archive. By exploiting the fact that projects that are built on
top of others will share some of their development history, we propose an
algorithm to arrange the list of all the repositories in the archive in
"fork cliques" (clusters of projects that are all forks of each others) and
"fork networks" (clusters of projects that are transitively linked together by
forking relationships). We compute these structures for the entire Software
Heritage graph and measure their size distributions.

# Applications

Having both a deeper understanding of the underlying structure of the graph as
well as a platform to run experiments makes it possible to try out different
scale-out approaches experimentally. We evaluate how "sharding" the data with
respect to different graph orderings (breadth-first order, layered label
propagation order, fork cliques and connected components) can allow for faster
parallel processing for common use cases.

The analysis platform can also be used to generate derived data from the graph.
As a case study, in order to construct an index that can efficiently find the
first occurrence of a given file in a repository, we showcase a tool to extract
a "filesystem diff" dataset, containing the deltas between the source trees of
subsequent commits.

Finally, we discuss future research directions and open subjects: supporting
general-purpose graph queries through an expressive query language, providing
more tooling to streamline scale-out analyses, as well as reducing the lag
between the public datasets and the live data through incremental graph
exports.

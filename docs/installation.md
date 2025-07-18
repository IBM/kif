# Installation

## PyPI

```
$ pip install kif-lib
```

## Sources

```
$ git clone https://github.com/IBM/kif.git
$ cd kif
$ pip install -e .
```

## (Optional) Jena support

Make sure you have both the Java run-time and [Apache
Jena](https://jena.apache.org/) installed.  Then all you need to do is
install [JPype](https://jpype.readthedocs.io/en/latest/):

```
$ pip install jpype1
```

To check whether the `sparql-jena` store is available and working, run the
following:

```
$ python -c 'import kif_lib; print(kif_lib.Store("sparql-jena"))'
<kif_lib.store.sparql.jena.JenaSPARQL_Store object at ...>
```

The above command should succeed as long as a working `jena` command is
available, e.g.,

```
$ jena
Jena version : 5.3.0
Jena home    : /usr/local/Cellar/jena/5.3.0/libexec
```

Or the `JENA_HOME` environment variable is set to the root directory of
Jena's distribution.

### Obtaining Jena

#### MacOS

Using [Homebrew](https://docs.brew.sh/):
```
$ brew install jena
```

#### Official release

Download the [latest release](https://jena.apache.org/download/index.cgi):

```
$ wget https://dlcdn.apache.org/jena/binaries/apache-jena-5.3.0.tar.gz
```

Unpack it:

```
$ tar -xf apache-jena-5.3.0.tar.gz
```

Set the `JENA_HOME` environment variable:

```
$ export JENA_HOME=$PWD/apache-jena-5.3.0/
```

## (Optional) QLever support

Make sure you have both the QLever index builder `IndexBuilderMain` and the
server `ServerMain` executables in your path.

To check whether the `sparql-qlever` store is available and working, run the
following:

```
$ python -c 'import kif_lib; print(kif_lib.Store("sparql-qlever"))'
<kif_lib.store.sparql.qlever.QLeverSPARQL_Store object at ...>
```

### Obtaining and installing QLever

#### MacOS

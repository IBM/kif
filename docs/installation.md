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

Make sure you have both the [QLever](https://qlever.cs.uni-freiburg.de/)
index builder `IndexBuilderMain` and the server `ServerMain` executables in
your path.

To check whether the `sparql-qlever` store is available and working, run the
following:

```
$ python -c 'import kif_lib; print(kif_lib.Store("sparql-qlever"))'
<kif_lib.store.sparql.qlever.QLeverSPARQL_Store object at ...>
```

### Obtaining and installing QLever

#### MacOS

Install [cmake](https://www.cmake.org/), [conan](https://conan.io), and
[llvm 17](https://llvm.org/):

```
$ brew install conan@2 llvm@17
```

Setup the LLVM environment:

```
$ export LLVM_HOME=$(brew --prefix llvm@17)
$ export PATH="${LLVM_HOME}/bin:$PATH"
$ export CPPFLAGS="-I${LLVM_HOME}/include"
$ export LDFLAGS="-L${LLVM_HOME}/lib"
```

Clone QLever's GitHub repository:

```
$ git clone https://github.com/ad-freiburg/qlever.git
$ cd qlever
```

Build and install the conan environment:

```
$ mkdir build
$ cd build
$ conan install .. -pr:b=../conanprofiles/clang-17-macos -pr:h=../conanprofiles/clang-17-macos -of=. --build=missing
$ cd ..
```

Run cmake to configure the project and generate a makefile:

```
$ cmake -B ./build\
  -DCMAKE_BUILD_TYPE=Release\
  -DCMAKE_TOOLCHAIN_FILE="${PWD}/build/conan_toolchain.cmake"\
  -DUSE_PARALLEL=true\
  -DRUN_EXPENSIVE_TESTS=false\
  -DENABLE_EXPENSIVE_CHECKS=false\
  -DCMAKE_CXX_COMPILER=clang++\
  -DADDITIONAL_COMPILER_FLAGS="-fexperimental-library"\
  -D_NO_TIMING_TESTS=ON\
  -DADDITIONAL_LINKER_FLAGS="-L${LLVM_HOME}/lib/c++"
```

Build the project:

```
$ source ./build/conanrun.sh
$ cmake --build ./build --config Release
```

If the above succeeds, it will generate the following binaries:

```
$ ls ./build/{IndexBuilderMain,ServerMain}
```

Now all you have to do is add them to your `PATH`.  Make sure to source
`./build/conanrun.sh` before running them.

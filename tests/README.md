# Running tests

* 1 test module; all benchmarks in it; all build types

```
python3 -d -m nose2 -s tests module_name

# e.g., to test all SPEC benchmarks
python3 -d -m nose2 -s tests test_spec

```

* 1 benchmark from a module; all build types

```
NAME=benchmark_name python3 -d -m nose2 -s tests module_name

# e.g., to test perlbench from SPEC
NAME=perlbench python3 -d -m nose2 -v -s tests test_spec
```

* 1 build type for all benchmarks in a module

```
ACTION=build_type python3 -d -m nose2 -s tests module_name

# e.g., to test gcc native build on SPEC
ACTION=gcc_native python3 -d -m nose2 -v -s tests test_spec
```

* 1 build type and 1 benchmark form a module

```
ACTION=build_type python3 -d -m nose2 -s tests module_name

# e.g., to test gcc native build on SPEC
ACTION=gcc_native python3 -d -m nose2 -v -s tests test_spec
```


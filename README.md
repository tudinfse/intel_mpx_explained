# Intel MPX Explained

A repository containing complete experimental setup of our "Intel MPX Explained" paper:

* `raw_results`: complete unprocessed measurements, in the form of `.csv` files.
* `asm_measurements`: scripts used to measure MPX instruction latencies and throughput.
Also, a set of scripts that prove existence of contention on Port 1.
* `src`: sources of the tested benchmark suits and case studies. (SPEC was excluded for licencing reasons)
* `experiments/exp_*_*/run.py`: scripts defining the experiment procedure
* `experiments/makefiles/`: build types
* `install`: installation scripts

UPDATE (04-02-2020): At this point, Intel MPX support is officially discontinued by GCC ([Patch](https://gcc.gnu.org/ml/gcc-patches/2018-04/msg01225.html)) and Linux ([Patch](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ccaaaf6fe5a5e1fffca5cca0f3fc4ec84d7ae752)). The technology won't be available on the future Intel processors too ([Announcement](https://software.intel.com/en-us/blogs/2013/07/22/intel-memory-protection-extensions-intel-mpx-support-in-the-gnu-toolchain)).

### Running the experiments

The interface is the same for all the benchmarks:

```sh
./fex.py run -n benchamark_name -t build_type --stats measurement_tool
```

For example, to measure performance on Phoenix:

```sh
./fex.py run -n phoenix_perf -t gcc_native icc_native clang_native gcc_asan gcc_asan_only_write clang_asan gcc_mpx gcc_mpx_only_write gcc_mpx_no_narrow_bounds gcc_mpx_no_narrow_bounds_only_write icc_mpx icc_mpx_only_write icc_mpx_no_narrow_bounds icc_mpx_no_narrow_bounds_only_write softbound_native softbound_enabled safecode_native safecode_enabled --stats perf
```

For the details of how to run the experiments, refer to the documentation of the [underlying Fex framework](https://github.com/tudinfse/fex).
Note that this repository uses a bit outdated version of Fex and some things may mismatch.
In such occasions, please, create an issue or contact me directly.

### Publications

Full description of this work can be found in one of the follwing:

* [Technical Report](https://arxiv.org/abs/1702.00719): complete results and full discussion
* [Supporting website](https://intel-mpx.github.io/): even more detailed results, but less discussion


### Cite us!

Paper:

```
@Article{Oleksenko:2018,
  author = {Oleksenko, Oleksii and Kuvaiskii, Dmitrii and Bhatotia, Pramod and Felber, Pascal and Fetzer, Christof},
  title = {{Intel MPX Explained: A Cross-layer Analysis of the Intel MPX System Stack}},
  journal   = "Proceedings of the ACM on Measurement and Analysis of Computing Systems (POMACS)",
  year = {2018},
}
```

Technical Report:

```
@Article{Oleksenko:2017,
  author = {Oleksenko, Oleksii and Kuvaiskii, Dmitrii and Bhatotia, Pramod and Felber, Pascal and Fetzer, Christof},,
  title = {{Intel MPX Explained: An Empirical Study of Intel MPX and Software-based Bounds Checking Approaches}},
  journal   = "",
  archivePrefix = "arXiv",
  eprint = {1702.00719},
  primaryClass = "",
  year = {2017},
}
```

==============================================================================
NOTE by Dmitrii Kuvaiskii:
  The license of PARSEC benchmark suite is complex, and each benchmark and
  each input have their own licenses; the full description is at:
      http://parsec.cs.princeton.edu/license.htm
  Some of the included programs and inputs are under GPL 2 or GPL 3 which
  precludes their inclusion in our framework.
==============================================================================



List of benchmarks:

Benchmark     | Language | Application Domain
--------------|----------|-------------------
blackscholes  |	C++	     | Financial Analysis
bodytrack	  | C++	     | Computer Vision
canneal	      | C++    	 | Engineering
dedup	      | C	     | Enterprise Storage
facesim       | C++      | Animation
ferret	      | C	     | Similarity Search
fluidanimate  | C++	     | Animation
raytrace	  | C++	     | Animation
streamcluster |	C++	     | Data Mining
swaptions	  | C++	     | Financial Analysis
vips	      | C++	     | Media Processing
x264	      | C	     | Video Compression

Not supported benchmarks:

Benchmark     | Language | Application Domain | Why skipped?
--------------|----------|----------------------------------
frequmine     | C++      | Data Mining        | based on OpenMP

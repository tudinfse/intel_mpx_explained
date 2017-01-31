NAME := iofuncs
SRC := object \
	meta \
	base64 \
	callback \
	debug \
	dispatch_types \
	error \
	im_binfile \
	im_close \
	im_cp_desc \
	im_demand_hint \
	im_generate \
	im_histlin \
	im_image \
	init \
	im_mapfile \
	im_open \
	im_open_vips \
	im_partial \
	im_prepare \
	im_setbuf \
	im_setupout \
	im_unmapfile \
	im_guess_prefix \
	sinkmemory \
	sinkscreen \
	sinkdisc \
	sink \
	im_wrapmany \
	im_writeline \
	memory \
	check \
	package \
	header \
	region \
	rect \
	semaphore \
	threadpool \
	util \
	im_init_world \
	buf \
	window \
	buffer \
	time

CFLAGS += -DPATH_MAX=4096 -DHAVE_SYS_MMAN_H -DHAVE_SYS_FILE_H -DHAVE_UNISTD_H -DHAVE_SYS_PARAM_H -DHAVE_REALPATH
CXXFLAGS += -DPATH_MAX=4096 -DHAVE_SYS_MMAN_H -DHAVE_SYS_FILE_H -DHAVE_UNISTD_H -DHAVE_SYS_PARAM_H -DHAVE_REALPATH

include ../subdirs_common.mk

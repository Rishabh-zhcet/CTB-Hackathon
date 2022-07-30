# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/mux.v

TOPLEVEL := mux          # design
MODULE   := test_mux     # test

include $(shell cocotb-config --makefiles)/Makefile.sim
.xml sim_build __pycache__ 
clean_all: clean
	rm -rf *

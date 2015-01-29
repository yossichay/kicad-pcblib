PYTHON ?= /usr/bin/python


IPC_LEAST_URL := http://www.freepcb.com/downloads/IPC7351-Least_v2.zip
IPC_MOST_URL := http://www.freepcb.com/downloads/IPC7351-Most_v2.zip
IPC_NOMINAL_URL := http://www.freepcb.com/downloads/IPC7351-Nominal_v2.zip

IPC_LEAST_NAME := IPC7351-Least_v2.zip
IPC_MOST_NAME := IPC7351-Most_v2.zip
IPC_NOMINAL_NAME := IPC7351-Nominal_v2.zip

ifeq ("$(wildcard $(IPC_LEAST_NAME))", "")
	IPC_LEAST := $(IPC_LEAST_URL)
else
	IPC_LEAST := $(IPC_LEAST_NAME)
endif

ifeq ("$(wildcard $(IPC_MOST_NAME))", "")
	IPC_MOST := $(IPC_MOST_URL)
else
	IPC_MOST := $(IPC_MOST_NAME)
endif

ifeq ("$(wildcard $(IPC_NOMINAL_NAME))", "")
	IPC_NOMINAL := $(IPC_NOMINAL_URL)
else
	IPC_NOMINAL := $(IPC_NOMINAL_NAME)
endif


.PHONY: ipcpretty 3d

ipcpretty: IPC7351-Least_v2.zip IPC7351-Most_v2.zip IPC7351-Nominal_v2.zip
	rm -rf IPC7351-Least.pretty
	mkdir IPC7351-Least.pretty
	${PYTHON} download_ipc.py \
		--3dmap config/3dmap --rounded-pad-exceptions config/rpexceptions \
		${IPC_LEAST} IPC7351-Least.pretty freepcb2pretty.py
	rm -rf IPC7351-Most.pretty
	mkdir IPC7351-Most.pretty
	${PYTHON} download_ipc.py --no-confirm-license \
		--3dmap config/3dmap --rounded-pad-exceptions config/rpexceptions \
		${IPC_MOST} IPC7351-Most.pretty freepcb2pretty.py
	rm -rf IPC7351-Nominal.pretty
	mkdir IPC7351-Nominal.pretty
	${PYTHON} download_ipc.py --no-confirm-license \
		--3dmap config/3dmap --rounded-pad-exceptions config/rpexceptions \
		${IPC_NOMINAL} IPC7351-Nominal.pretty freepcb2pretty.py

IPC7351-Least_v2.zip:
	wget ${IPC_LEAST}

IPC7351-Most_v2.zip:
	wget ${IPC_MOST}

IPC7351-Nominal_v2.zip:
	wget ${IPC_NOMINAL}

3d:
	rm -rf 3d
	${PYTHON} download_3d.py

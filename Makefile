#.SILENT:
SHELL = /bin/bash


all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"readFile_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
"

VERSION := "0.0.2"
BRANCH := $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')

pack: make_build
	rm -f readFile-*.tar.gz
	echo Create archive \"readFile-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../readFile-$(VERSION)-$(BRANCH).tar.gz readFile writeFile read_file_venv

clean_pack:
	rm -f readFile-*.tar.gz


readFile.tar.gz: build
	cd make_build; tar czf ../readFile.tar.gz readFile writeFile read_file_venv && rm -rf ../make_build

build: make_build

make_build:
	# required section
	echo make_build
	mkdir make_build
	cp -R ./readFile make_build
	cp -R ./writeFile make_build
	cp *.md make_build/readFile/
	cp *.md make_build/writeFile/

	mkdir -p make_build/read_file_venv/lib/python3.9/site-packages
	cp -R ./df_storage  make_build/read_file_venv/lib/python3.9/site-packages


clean_build:
	rm -rf make_build

venv:
	echo Create venv;
	conda create --copy -p ./venv -y
	conda install -p ./venv python==3.9.7 -y
	./venv/bin/pip install --no-input  postprocessing_sdk@git+ssh://git@github.com/ISGNeuroTeam/postprocessing_sdk.git@develop

clean_venv:
	rm -rf ./venv

pp_cmd: venv
	./venv/bin/pp_sdk createcommandlinks


dev: pp_cmd
	ln -s -r ./readFile pp_cmd/readFile

clean: clean_build clean_pack clean_test clean_venv

test:
	@echo "Testing..."

clean_test:
	@echo "Clean tests"
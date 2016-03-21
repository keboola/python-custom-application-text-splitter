#!/bin/sh

export KBC_DATA_DIR=./test/data
py.test --cov=text_splitter --cov-report term-missing

read

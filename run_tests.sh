#!/bin/sh

export KBC_DATA_DIR=./test/data
py.test --cov=textSplitter --cov-report term-missing

read

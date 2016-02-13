#!/bin/bash

if [ ${#} != 1 ]; then
    printf "${0}: Wrong number of arguments\n"
    exit
fi

if [ -d ${1} ]; then
    rm -rf ${1}
    mkdir ${1}
else
    mkdir ${1}
fi


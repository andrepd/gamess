#!/bin/bash

for i in $(ls *.inp)
do
    name=$(echo $i | cut -f 1 -d '.')
    rungms ${name} | tee ${name}.log
done

rm *.inp
rm *.dat

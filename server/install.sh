#!/bin/sh
while read module; do
  pip install $module
  echo $module 
done < requirements.txt
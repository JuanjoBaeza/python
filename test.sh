#!/bin/bash
# Test for failure

#cat "$1"
#if [ "$?" -ne "0" ]; then
#echo "Error: Reading $1 failed."
#fi

if [ -r "$1" ]; then
cat "$1"
else
echo "Error: $1 is not a readable file."
fi


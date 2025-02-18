#!/bin/bash

prevRev=`git rev-parse HEAD~`
url=`git config --get remote.origin.url`

git clone https://github.com/kbranch/LogicTester.git

cd LogicTester
git clone ${url} LADXR

cd LADXR
git reset --hard ${prevRev}

cd ..

ln -s ../logic newLogic
touch diffs.log
python3 main.py
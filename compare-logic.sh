#!/bin/bash

prevRev=`git rev-parse HEAD~`
url=`git config --get remote.origin.url`

git clone https://github.com/kbranch/LogicTester.git
git checkout actions-v2
cd LogicTester

git clone ${url} LADXR
cd LADXR
git reset --hard ${prevRev}

cd ..

touch diffs.log
python3 main.py --reference-ladxr-path "LADXR" --new-logic-path "../logic"
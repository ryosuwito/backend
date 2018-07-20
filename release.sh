#!/bin/bash

set -e
set -x

USAGE="$0 VERSION. For example, $0 1.0.8"
if [ $# -lt 1 ]; then
    echo $USAGE
    exit 1
fi
DIR=website.$1
rsync -avz --exclude ".git" --exclude release.sh ./ root@website:local/install/$DIR/
echo "making sym link ..."
#ssh root@website "cd local/install/; rm dtl_web; ln -s $DIR dtl_web; cd $DIR; ln -sf ../db.sqlite3; ln -s ../media; cd main; rm -rf media; ln -s ../../media"
ssh root@website "cd local/install/; rm dtl_web; ln -s $DIR dtl_web; cd $DIR; ln -sf ../db.sqlite3; cd media; ln -s ~/local/install/resumes"

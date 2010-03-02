#!/bin/bash

dir=`dirname $0`
cd $dir
dir=`pwd`
cd -

rm $dir/*.zip
for i in sample_animals transport; do
  (cd ~/.babyslam/sets; zip -r $dir/$i.zip $i)
done

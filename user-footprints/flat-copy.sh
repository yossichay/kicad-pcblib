#!/bin/sh
#

# counter
i=0

# put your new directory here
# can't be similar to dir_*, otherwise bash will
# expand it too
mkdir newdir

for file in `ls`; do
    # gets only the name of the file, without directory
    fname=`basename $file`
    # gets just the file name, without extension
    name=${fname%.*}
    # gets just the extention
    ext=${fname#*.}

    # get the directory name
    dir=`dirname $file`
    # get the directory suffix
    suffix=${dir#*_}

    # rename the file using counter
    fname_counter="${name}_$((i=$i+1)).$ext"

    # rename the file using dir suffic
    fname_suffix="${name}_$suffix.$ext"

    # copy files using both methods, you pick yours
    cp $file "newdir/$fname_counter"
    cp $file "newdir/$fname_suffix"
done

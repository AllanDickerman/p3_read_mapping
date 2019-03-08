# working with the most recent download directory for mlst data, update directory path as needed 
# create new directory with subdirectories for each species (or group)
# generate kma index for each species in its directory
# also copy the profile file into that directory (redundant, but makes this data source independent of original directory)
# the kma source code is agailable at: https://bitbucket.org/genomicepidemiology/kma.git

pathToMlstDownloads=/vol/patric3/downloads/mlstdb-2019-0221

datadir=`basename $pathToMlstDownloads`
datadir=${datadir}_kma_indexes
mkdir $datadir

cp $pathToMlstDownloads/metadata.txt $datadir

for f in $pathToMlstDownloads/seq/*
do sp=`basename $f`
    mkdir $datadir/$sp
    cat $pathToMlstDownloads/seq/$sp/*fna | kma index -i -- -o $datadir/$sp/${sp}_kma -NI
    cp $pathToMlstDownloads/pro/$sp.pro.txt $datadir/$sp
done

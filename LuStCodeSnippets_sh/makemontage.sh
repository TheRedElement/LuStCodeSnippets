#!/bin/bash

make_montage_pdf () {
    #   - function to create a pdf-montage of a set of input images
    #
    #Usage
    #-----
    #   ```bash
    #   source makemontage.sh
    #   make_montage_pdf "*.jpg" 6 6 montage.pdf 16384 2
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`files`)
    #       - `string`
    #       - files to use for creating the montage
    #       - glob-patterns are supported
    #   - $2 (`nrows`)
    #       - `integer`
    #       - number of rows to use in the montage per page
    #   - $3 (`ncols`)
    #       - `integer`
    #       - number of columns to use in the montage per page
    #   - $4 (`outname`)
    #       - `string`
    #       - name of the outputfile to be produced
    #   - $5 (`numpixels`)
    #       - `integer`
    #       - number of pixels each image shall be resized to
    #       - denotes the area in units of pixels
    #   - $6 (`pad`)
    #       - `integer`
    #       - number of pixels to use as padding around each image
    #
    #Example
    #-------
    #   ```bash
    #   make_montage_pdf "*.jpg" 6 6 montage.pdf 16384 2
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   Processing 266 files with batchsize 36 (8 batches)
    #   resizing...
    #   Processing batch 1/8 (1-37, temporary filename: page_1.png)
    #   Processing batch 2/8 (37-73, temporary filename: page_2.png)
    #   Processing batch 3/8 (73-109, temporary filename: page_3.png)
    #   Processing batch 4/8 (109-145, temporary filename: page_4.png)
    #   Processing batch 5/8 (145-181, temporary filename: page_5.png)
    #   Processing batch 6/8 (181-217, temporary filename: page_6.png)
    #   Processing batch 7/8 (217-253, temporary filename: page_7.png)
    #   Processing batch 8/8 (253-289, temporary filename: page_8.png)
    #   ```

    #input parameters
    local files=($1)   #expand into array
    local nrows=$2
    local ncols=$3
    local outname=$4
    local resize=$5
    local pad=$6


    #infered parameters
    local nfiles=${#files[@]}                               #get number of files
    local batchsize=$((nrows * ncols))                      #get batchsize from layout
    local nbatches=$(((nfiles + batchsize) / batchsize))    #get number of batches #add one batchsize to ensure everything gets processed
    local pages=()                                          #init array of pages

    # echo "${files[@]:1:$batchsize}"
    echo "Processing ${nfiles} files with batchsize ${batchsize} (${nbatches} batches)"

    #resize images
    echo "resizing..."
    tempdir=./temp_resized/
    mkdir -p $tempdir
    mogrify -resize "${resize}@" -path $tempdir $1

    #overwrite `files` with temporary imgaes
    files=($tempdir*)

    #process in batches of `batchsize`
    for batchidx in $(seq 1 $nbatches); do
        startidx=$((((batchidx-1)*batchsize)+1))
        batch=${files[@]:$startidx:$batchsize}
        pagename="page_$batchidx.png"                                                   #name of page
        echo "Processing batch $batchidx/$nbatches ($startidx-$((startidx+batchsize)), temporary filename: ${pagename})"  #verbosity
        
        #combine
        montage $batch -tile ${ncols}x${nrows} -geometry +${pad}+${pad} ${pagename}     #create montage of current batch
        
        #add to pages
        pages+=(${pagename})                                                            #append to array of pages

    done

    #combine into pdf
    convert "${pages[@]}" "$outname"

    #cleanup
    rm -f "${pages[@]}"
    rm -r $tempdir
}


make_montage_pdf "*.jpg" 6 6 montage.pdf 16384 2
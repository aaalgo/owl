# owl
image annotation app

### Python3 and PicPac

We have recently migrated to Python3.

OWL requires picpac.  If you are using Ubuntu 16.04, you can
[download](http://www.aaalgo.com/picpac/binary/picpac.cpython-35m-x86_64-linux-gnu.so)
a pre-built picpac binary to the owl directory.

### Notes

1. Before starting, copy params.py.example to params.py under annotate,
   and modify that file to suit your needs.
2. Usually "images" is a link to the directory which holds your images.
   When images are large, one usually keep two directories with the same
   filenames but different resolutions.  Point symbolic link "images" to
   the small version when you do import & annotation.  After annotation
   is done, symbolic link "images" to the full version and do
   `./manage.py export db`.
3. To avoid copying a large db from local annotation side to server side. After annotation, just copy "db.sqlite3" to owl directory on your destination. 
   Make sure you have the same "images" (image file names must be the same, but you can keep different resolution) there. Then do `./manage.py export db`
   
   

### Start annotation
  1. `./rebuild.sh`
  2. `./run.sh`   
  3. Go to http://localhost:8005/annotate/ to do annotation.   
  4. After annotation, do:   
     `./manage.py export db`



### Manage db with [picpac](https://github.com/aaalgo/picpac)

##### Merge db
   `picpac-merge output input1 input2 input3 ...`

##### Split db

   `picpac-kfold --split 10 --stratify 1 --max-test 500 input output`   
   This will split all data into 10 parts, using one part for testing.  If test image exeeds 500 it will use only 500 for testing and put the rest in training. "output.train" and "output.test" will be generated as training and validation db.

##### View db and annotation

   `picpac-explorer db`  
   View database at port 18888.  
   Go to "stream" channel, choose "Json" for "annotation", then "Reload" data



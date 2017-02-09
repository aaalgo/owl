# owl
image annotation app

Notes:

1. Before starting, copy params.py.example to params.py under annotate,
   and modify that file to suit your needs.
2. Usually "images" is a link to the directory which holds your images.
   When images are large, one usually keep two directories with the same
   filenames but different resolutions.  Point symbolic link "images" to
   the small version when you do import & annotation.  After annotation
   is done, symbolic link "images" to the full version and do
   "./manage.py export db".


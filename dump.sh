#!/bin/bash

sqlite3 db.sqlite3 <<FOO
.mode tabs
.headers off
select path, meta, anno from annotate_image as I, annotate_annotation as A
    where I.id = A.image_id and I.done <> 0;
FOO

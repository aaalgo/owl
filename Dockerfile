from ubuntu:16.04
RUN apt-get update && apt-get install -y python3-pip git wget
RUN pip3 install django django_extensions simplejson
RUN cd / && git clone https://github.com/aaalgo/owl
RUN cd /owl && wget http://www.aaalgo.com/picpac/binary/picpac.cpython-35m-x86_64-linux-gnu.so

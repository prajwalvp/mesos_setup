# Pikasoup

Pulsar Search Pipeline based on Peasoup and a pika wrapper. 

Usage :

For publishing to RabbitMQ server

nvidia-docker run -i -v [path on host of input files]:[path in container] [docker_image_name] python3 publish.py -H [host ip] -P [port number] -Q [name of queue] --path=[path in container of mounted files]

example : docker run -i -v /test_vectors/:/input/ pikasoup python3 publish.py -H 134.104.70.93 -p 31861 -q peasoup_1 --log_level info --path=/input 


For consuming to RabbitMQ server


docker run -i -v [path on host of input files]:[path in container] -v [path on host of output to be written]:[path in container] [docker_image_name] python3 publish.py -H [host ip] --input=[name of queue] --path=[path in container of output files]


example: docker run -i -v /input_vectors/:/input/-v /output_vectors/:/output/ pikasoup python3 consume.py -H 134.104.70.93 --input=peasoup_1 -p 31861 --path=/output



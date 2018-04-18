# Pikasoup

Pulsar Search Pipeline based on Peasoup and a pika wrapper. 

Usage :

For publishing to RabbitMQ server

nvidia-docker run -i -v <path on host of input files>:<path in container> <docker_image_name> python3 publish.py -host <host ip> -queue <name of queue> -path <path in container of mounted files>


example: nvidia-docker run -i -v /tmp:/software/test_vectors python3 publish.py -host 172.17.0.7 -queue test3 -path /software/test_vectors


For consuming to RabbitMQ server


nvidia-docker run -i -v <path on host of input files>:<path in container -v <path on host of output to be written>:<path in container> <docker_image_name> python3 publish.py -host <host ip> -queue <name of queue> -path <path in container of output files>


example: nvidia-docker run -it -v /beegfs/prajwal/test_vectors:/software/test_vectors -v /beegfs/prajwal/peasoup_output:/software/peasoup_output pikasoup python3 consume.py -host 172.17.0.7 -queue test3 -path /software/peasoup_output


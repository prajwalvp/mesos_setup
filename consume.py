import pika
import os
import sys
import json
from subprocess import call



i=1
# Setup pika connection 
while True:
        if sys.argv[i]=='-host':
                hostname=sys.argv[i+1]
                i=i+2
        if sys.argv[i]=='-queue':
                queuename=sys.argv[i+1]
                i=i+2
        if sys.argv[i]=='-path':
                path=sys.argv[i+1]
                break

def receive():
    parameters = pika.ConnectionParameters(hostname)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename)
    method_frame, header_frame, body = channel.basic_get(queue = queuename)
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        data = json.loads(body.decode("utf-8"))
        return data


while True:
        try:
                info = receive();
                script1= "mkdir %s/%s" %(path,info['filename'])
                script1 = "peasoup -i %s -o %s/%s" %(info['input path']+'/'+info['filename'],path,info['filename'])
                call(script1,shell=True)
                print(info['filename'] + ' processed')
        except AttributeError:
                print('No more messages in broker!')
                break


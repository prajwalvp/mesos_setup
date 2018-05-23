import pika
import os
import sys
import json
from subprocess import call
import time
import optparse

def receive(options):

    credentials= pika.PlainCredentials('guest','guest')
    parameters = pika.ConnectionParameters(options.hostname,31861,'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=options.queuename)
    method_frame, header_frame, body = channel.basic_get(queue=options.queuename)
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        data = json.loads(body.decode("utf-8"))
        return data


def main():
    parser = optparse.OptionParser()
    parser.add_option('-H','--host',dest="hostname")
    parser.add_option('-Q','--queue',dest="queuename")
    parser.add_option('-p','--path',dest="file_path")
    options,remainder = parser.parse_args()
    while True:
        try:
            info = receive(options);
            script1= "mkdir %s/%s" %(options.file_path,info['filename'])
            script2 = "peasoup -i %s -o %s/%s" %(info['input path']+'/'+info['filename'],options.file_path,info['filename'])
            call(script1,shell=True) 
            call(script2,shell=True)
            print(info['filename'] + ' processed')
        except AttributeError:
            print('No more messages in broker!')
            time.sleep(5)
            continue

if __name__ == '__main__':
    main()

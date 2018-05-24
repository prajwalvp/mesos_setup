import pika
import json
import glob
import sys
import optparse



# Pass arguments 
parser = optparse.OptionParser()
parser.add_option('-H','--host',dest="hostname")
parser.add_option('-Q','--queue',dest="queuename")
parser.add_option('-p','--path',dest="file_path")

options,remainder = parser.parse_args()



# Pika setup
credentials = pika.PlainCredentials('guest','guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(options.hostname,31861,'/',credentials))  
channel = connection.channel()
channel.queue_declare(queue=options.queuename)


#Find all filterbank files
all_filterbank = glob.glob(options.file_path+'/'+'*.fil')
print(all_filterbank)
filterbank=[]
for i in all_filterbank:
    filterbank.append(i.strip(options.file_path+'/'))



# Publish to RabbitMQ
for i in range(len(all_filterbank)):
    data={"project_id":"PMPS","filename":filterbank[i],"input_path":options.file_path}
    message = json.dumps(data).encode('utf-8')
    channel.basic_publish(exchange='',routing_key=options.queuename,body=message)
    print("  Sent data! %d" %i)

connection.close()

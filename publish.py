import pika
import json
import glob
import sys

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



#print(hostname)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))  # hostname 
channel = connection.channel()



channel.queue_declare(queue=queuename)            # queue name

all_filterbank = glob.glob(path+'/'+'*.fil')

print(all_filterbank)

filterbank=[]
for i in all_filterbank:
    filterbank.append(i.replace(path+'/',''))




for i in range(len(all_filterbank)):
    data={"project id":"PMPS","filename":filterbank[i],"input path":path}
    message = json.dumps(data).encode('utf-8')
    channel.basic_publish(exchange='',routing_key=queuename,body=message)
    print("  Sent data! %d" %i)

connection.close()


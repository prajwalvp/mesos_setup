import pika
import json
import glob
import sys
import optparse
import pika_process
from optparse import OptionParser


# Pass arguments 


def main(opts):
    #credentials = pika.PlainCredentials('guest','guest')
    #connection = pika.BlockingConnection(pika.ConnectionParameters(options.hostname,31861,'/',credentials))  
    #channel = connection.channel()
    #channel.queue_declare(queue=options.queuename)
    producer = pika_process.pika_producer_from_opts(opts)
    all_filterbank = glob.glob(opts.file_path+'/'+'*.fil')
    print(all_filterbank)
    filterbank=[]
    for i in all_filterbank:
        filterbank.append(i.strip(opts.file_path+'/'))

    for i in range(len(all_filterbank)):
        data={"project_id":"PMPS","filename":filterbank[i],"input_path":opts.file_path}
        message = json.dumps(data).encode('utf-8')
        print("  Sending data! %s"%message)
        producer.publish(message)
        print("  Sent data! %d" %i)

if __name__=='__main__':
    parser = optparse.OptionParser()
    pika_process.add_pika_producer_opts(parser)
    parser.add_option('--path',dest="file_path")
    opts,args = parser.parse_args()

    main(opts)

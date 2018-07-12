import pika
import os
import sys
import json
from subprocess import call
import time
import pika_process
import optparse

def on_message(body,opts):
    info = json.loads(body.decode("utf=8"))
    script1 = "mkdir %s/%s" %(opts.output_file_path,info['filename'])
    script2 = "peasoup -i %s -o %s/%s" %(info['input_path']+'/'+info['filename'],opts.output_file_path,info['filename']) 
    print("Making directory for %s" %info['filename'])
    call(script1,shell=True)
    print("Made directory for %s" %info['filename'])
    print("Processing %s with peasoup" %info['filename'])
    call(script2,shell=True)
    print("%s has been processed" %info['filename']) 

    

def main(opts): 
    processor = pika_process.pika_process_from_opts(opts)  
    processor.process(lambda message: on_message(message, opts))

         
if __name__ == '__main__':
    parser = optparse.OptionParser()
    pika_process.add_pika_process_opts(parser)
    parser.add_option('--path',dest="output_file_path")
    opts,args = parser.parse_args()
    main(opts)

import json
import subprocess
import glob
import pika
import pika_process
import optparse



def on_message(body,opts):
    folding_packet = json.load(f)
    subprocess.check_call(["prepfold","-topo","-start","0.5","-p",str(folding_packet['period']),"-pd",str(folding_packet['pdot']),"-dm",str(folding_packet['dm']),str(folding_packet['file path'])])



def main(opts):
    processor = pika_process.pika_process_from_opts(opts)
    processor.process(lambda message: on_message(message, opts))
if __name__ == '__main_':
    parser = optparse.OptionParser()
    pika_process.add_pika_process_opts(parser)
    parser.add_option('--path',dest="output_file_path")
    opts,args = parser.parse_args()
    main(opts)

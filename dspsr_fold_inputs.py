import pika
import json
import subprocess
import glob
import pika_process
import optparse

def on_message(body,opts):
    folding_packet = json.load(f)
    with open('%s.txt'%(candidate[:-3]),'w') as f:
        f.write('SOURCE: %s\n'%folding_packet['source'])
        f.write('PERIOD: %s\n'%folding_packet['period'])
        f.write('DM: %s\n'%folding_packet['dm'])
        f.write('ACC: %s\n'%folding_packet['acc'])
        #f.write('RA: %s\n'%ra)
        #f.write('DEC: %s\n'%dec)
        #f.write('EPOCH: %s'str(epoch_start +0.5*no_of_samples*tsamp)) 
        f.close()

    ## Execute DSPSR ##

    #for cand_file in glob.glob('*.txt'):    
    #subprocess.check_call(["dspsr","J1857+0943.fil","-c",str(period[0]),"-D",str(dm[0]),"-k","parkes","-b","128","-L","10","-A","-O","first_out"])
        #subprocess.check_call(["dspsr","-P",cand_file,path_file_name])
    print "dspsr -P %s.txt %s" %(candidate[:-3],folding_packet['file path'])
    subprocess.check_call(["dspsr","-P",cand_file,folding_packet['file path']])
        #subprocess.check_call(["dspsr","-P",cand_file,'filterbank/J1857+0943.fil'])

def main(opts):
    processor = pika_process.pika_process_from_opts(opts)
    processor.process(lambda message: on_message(message, opts))


if __name__ == '__main__':
    parser = optparse.OptionParser()
    pika_process.add_pika_process_opts(parser)
    parser.add_option('--path',dest="output_file_path")
    opts,args = parser.parse_args()
    main(opts)

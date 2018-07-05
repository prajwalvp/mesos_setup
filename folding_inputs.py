import glob
import xml.etree.ElementTree as ET
import subprocess
import optparse
from optparse import OptionParser
import pika
import pika_process
import json

def period_modified(p0,pdot,no_of_samples,tsamp,fft_size):
    if (fft_size==0.0):
        return p0 - pdot*float(1<<(no_of_samples.bit_length()-1))*tsamp/2
    else:
        return p0 - pdot*float(1<<fft_size)*tsamp/2

def a_to_pdot(P_s, acc_ms2):
    LIGHT_SPEED = 2.99792458e8                 # Speed of Light in SI
    return P_s * acc_ms2 /LIGHT_SPEED


def middle_epoch(epoch_start, no_of_samples, tsamp):
     return epoch_start +0.5*no_of_samples*tsamp 

def main(opts):
    all_xml_files = glob.glob('*.xml') # needs to be changed for recursive reading 
    mod_period=[]
    period = []
    dm= []
    acc=[]
    pdot=[]
    for xml_file in all_xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

    # Header Parameters
        ra = root.find('header_parameters/src_raj').text
        dec = root.find('header_parameters/src_dej').text     
        source_name = root.find('header_parameters/source_name').text    
        source_name = source_name.replace(" ","").replace(":","").replace(",","")
        raw_data_filename=root.find('header_parameters/rawdatafile').text 
        epoch_start = float(root.find("header_parameters/tstart").text)
        tsamp = float(root.find("header_parameters/tsamp").text)
        no_of_samples = int(root.find("header_parameters/nsamples").text)

    #Search Parameters
        path_file_name = root.find("search_parameters/infilename").text
        fft_size = float(root.find('search_parameters/size').text)

        for DM in root.findall("candidates/candidate/dm"):
            dm.append(float(DM.text))

        for P in root.findall("candidates/candidate/period"):
            period.append(float(P.text))
        for A in root.findall("candidates/candidate/acc"): 
            acc.append(float(A.text))
    
        for i in range(len(period)):
            Pdot = a_to_pdot(period[i],acc[i])
            mod_period.append(period_modified(period[i],Pdot,no_of_samples,tsamp,fft_size))
            pdot.append(Pdot)

    
    

    # Fold topocentrically and with corrected period!
    
        for i in range(int(opts.no_of_candidates)):
            folding_packet={}
            folding_packet['source'] = source_name
            folding_packet['period'] = mod_period[i]
            folding_packet['dm'] = dm[i]
            folding_packet['acc'] = acc[i]
            folding_packet['pdot'] = pdot[i] 
            folding_packet['ra'] = ra
            folding_packet['dec'] = dec
            folding_packet['middle epoch'] = middle_epoch(epoch_start, no_of_samples, tsamp)
            folding_packet['file path'] = path_file_name 

            #with open('%s_cand_%d.json'%(source_name,i+1),'w') as f:

            producer = pika_process.pika_producer_from_opts(opts)
            message = json.dumps(folding_packet).encode('utf-8')
            print ("Sending candidate %s info for folding..."%i)
            producer.publish(message)
            print("Sent candidate %d"%i)
             
            #f.close()

if __name__=='__main__':
    parser = optparse.OptionParser()
    pika_process.add_pika_producer_opts(parser)
    parser.add_option('-N',type=str,help='Number of candidates to be folded',dest="no_of_candidates")
    opts,args = parser.parse_args()
    main(opts)

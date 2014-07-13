'''
This script supposed to extract audio, from rtp packets.
It depends on various networking, packet capturing tools
like pcapsipdump, tshark, pcaputil, dpkt python package etc.
It meant to run periodically, to do that set it up as cron
job
'''

import dpkt
import os
import glob
import time

# Otherthan Ethernet will not work.

PCAP2WAV="pcaputil"					## required, could be found at pjsip library
WORKDIR="/home/rakib/Documents/codezz/soip/rtptools/"	## change as per your need

#tshark -nr rtp.pcap -R rtp -T fields -e rtp.payload 

def execcmd(cmd):
	#now = time.strftime("%Y:%m:%d:%H:%M:%S")
	#newcmd = cmd + "> callcap.log 2>&1"
	print cmd
	return os.system(cmd)

''' run tshark and prepare packet for analysis '''
def preparepkt():
	flist = glob.glob("dump/*.pcap")
	for efile in flist:
		(path, name) = os.path.split(efile)
		cmd = "tshark -nr " + efile + " -R rtp -w " + "prepared/" + name
		print cmd
		ret = execcmd(cmd)

def actionpkt():
	flist = glob.glob("prepared/*.pcap")
	for efile in flist:
		for ts, pkt in dpkt.pcap.Reader(open(efile,'r')):
		    eth = dpkt.ethernet.Ethernet(pkt) 
		    
		    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
		       continue

		    ip = eth.data
		    ofile = efile

		    if ip.p == dpkt.ip.IP_PROTO_UDP:
	            	    (path, name) = os.path.split(efile)
			    (shortname, ext) = os.path.splitext(name)
			    udp = ip.data
			    part1 = "audio/" + shortname + "_1.wav"
			    cmd = PCAP2WAV + " --src-port=" + str(udp.sport) + " --dst-port="
			    cmd += str(udp.dport) + " " + efile + ' ' + part1
			    #print cmd
			    execcmd(cmd)

			    # Get the other way of sound
			    part2 = "audio/" + shortname + "_2.wav"
			    cmd = PCAP2WAV + " --src-port=" + str(udp.dport) + " --dst-port=" + str(udp.sport)
			    cmd += " " + efile + ' ' + part2 
			    execcmd(cmd)
			    # Now merge the files
			    if os.system.exist(part2) == True and os.system.exist(part1) == True:
				    cmd = "sox -m "
				    cmd += part1 + " " + part2 + " " + "audio/" + shortname + ".wav"
				    #print cmd
				    execcmd(cmd)
			    	    # remove partial files
			    	    #print part1, part2
			    	    os.remove(part2)
			    	    os.remove(part1)

				    # Convert to mp3 requires lame "lame -S -b 32 --resample 8 -a new.wav new.mp3"
				    cmd = "lame -S -b 32 --resample 8 -a " + "audio/" + shortname + ".wav " + "audio/" + shortname + ".mp3"
				    #print cmd
				    execcmd(cmd)
				    path = "audio/"+ shortname + ".wav"
				    os.remove(path)
				    cmd = "mv -f " + efile + " processed/"
				    execcmd(cmd)
			    	    break
			   if os.system.exist(part1) == False:
				    path = "audio/" + shortname + "_2.mp3"
				    cmd = "lame -S -b -32 --resample 8 -a " + part2 + " " + shortname + " " + path
				    execcmd(cmd)
				    os.remove(part2)
			   	    break
			   if os.system.exist(part2) == False:
				    path = "audio/" + shortname + "_1.mp3"
				    cmd = "lame -S -b -32 --resample 8 -a " + part1 + " " + shortname + " " + path
			            execcmd(cmd)
				    os.remove(part1)
			   	    break

def cleardump():
	flist = glob.glob("dump/*")
	for ef in flist:
		os.remove(ef)

if __name__ == "__main__":
	os.chdir(WORKDIR)
	if os.path.exists("dump") == False:
		os.system("mkdir dump")

	if os.path.exists("audio") == False:
		os.system("mkdir audio")

	if os.path.exists("prepared") == False:
		os.system("mkdir prepared")

	if os.path.exists("processed") == False:
		os.system("mkdir processed")

	# Craft prepare directory
	pcapdir = time.strftime("%Y%m%d") + "/" + time.strftime("%H")
	# pcapsipdump by default directory
	cmd = "cp -rf " + "/var/spool/pcapsipdump/" + pcapdir + "/*" + " dump/"
	#print cmd
	#cmd = "rm -rf " + pcapdir + "/*"
	#print cmd
	os.system(cmd)
	''' TODO: move packets into dump directory '''
	preparepkt()
	actionpkt()
	cleardump()

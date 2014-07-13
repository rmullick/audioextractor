audioextractor
==============

A simple script to automate audio extraction from rtp packets.

This script supposed to extract audio, from rtp packets.
It depends on various networking, packet capturing tools
like pcapsipdump, tshark, pcaputil, dpkt python package etc.
It meant to run periodically, to do that set it up as cron
job.

Required tools are sox, lame, tshark, pcaputil (from pjsip).
pcapsipdump is used to capture sip/rtp packets, needs to be
deployed and dpkt python module is required.

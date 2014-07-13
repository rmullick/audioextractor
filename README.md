audioextractor
==============

A simple script to automate audio extraction from rtp packets.

This script supposed to extract audio, from rtp packets.
It depends on various networking, packet capturing tools
like pcapsipdump, tshark, pcaputil, dpkt python package etc.
It meant to run periodically, to do that set it up as cron
job.

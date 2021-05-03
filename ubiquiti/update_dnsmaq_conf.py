#!/usr/bin/python2

"""Append Netflix blocks to dns dnsmasq.conf

Make this file executable and place in the `/config/scripts/post-config.d#` directory

It's Python2 because that's all Ubiquti OS has as of right now.
"""


import subprocess


def main():
    """
    Do the needful
    """

    netflix_blocks = """
# Null AAAA response on these domains
server=/netflix.com/#
address=/netflix.com/::
server=/netflix.net/#
address=/netflix.net/::
server=/nflxext.com/#
address=/nflxext.com/::
server=/nflximg.net/#
address=/nflximg.net/::
server=/nflxvideo.net/#
address=/nflxvideo.net/::
server=/nflxso.net/#
address=/nflxso.net/::
server=/amazonaws.com/#
address=/amazonaws.com/::
"""
    dnsmasq_conf_location = "/etc/dnsmasq.conf"

    # Append the requsite Netflix AAAA blocks
    with open(dnsmasq_conf_location, "a") as dnsmasq_conf_file:
        dnsmasq_conf_file.write(netflix_blocks)
    
    # Restart DNSMasq
    subprocess.call(["/etc/init.d/dnsmasq", "restart"])


if __name__ == "__main__":
    main()

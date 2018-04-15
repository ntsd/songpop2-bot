import pyshark

rtp_list = []
#cap = pyshark.FileCapture('/Users/bwarner/PycharmProjects/socketstuff/sith.pcap', display_filter='rtp')
cap = pyshark.LiveCapture(interface='eth0')
##raw_audio = open('my_audio.wav','wb')
for i in cap:
    try:
        rtp = i[3]
        if rtp.payload:
             print(rtp.payload)
             rtp_list.append(rtp.payload.split(":"))
    except:
        pass
print(rtp_list)
##for rtp_packet in rtp_list:
##    packet = " ".join(rtp_packet)
##    print(packet)
##    audio = bytearray.fromhex(packet)
##    raw_audio.write(audio)

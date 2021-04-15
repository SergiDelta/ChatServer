##########################################################
#                                                        #
# Author: Sergio Garcia Lopez                            #
#                                                        #
# GitHub: https://github.com/SergiDelta/ChatServer       #
#                                                        #
# Date: April 2021                                       #
#                                                        #
# Description: Client programm example for ChatServer.py #
#                                                        #
##########################################################

import socket
import sys
import select

if len(sys.argv) != 3:
   print("Use: " + sys.argv[0] + " <host> " + "<port>")
   sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
   print("Trying to connect...")
   s.connect((host,port))

except socket.error as e:
   print(e)
   sys.exit()

print("Connected")

try:

   while True:

      try:

         rlist, wlist, xlist = select.select([s], [], [], 0.5)

         if [rlist, wlist, xlist] != [ [], [], [] ]:

            rx_msg = s.recv(1024)
            rx_decoded = rx_msg.decode()

            if rx_decoded[ len(rx_decoded) - 1 ] == '\n':
               rx_list = list(rx_decoded)
               rx_list[ len(rx_decoded) - 1 ] = ''
               rx_decoded = ''.join(rx_list)

            print(rx_decoded)

            if rx_decoded.find("Timeout") != -1:
               break

         tx_msg = input(">> ")
         s.sendall( (tx_msg + "\n").encode() )

      except socket.error:
         break

except KeyboardInterrupt:
   print()

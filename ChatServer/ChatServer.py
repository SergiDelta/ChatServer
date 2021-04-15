#####################################################
#						    #
# Author: Sergio Garcia Lopez                       #
#			    			    #
# GitHub: https://github.com/SergiDelta/ChatServer  #
#                                                   #
# Date: April 2021				    #
#				                    #
# Description: Simple chat server that uses threads #
#   to handle TCP connections. It includes chat     #
#   records, timeout handling and broadcasting.     #
#						    #
#####################################################

import socket
import sys
import threading
import datetime
import re

timeout = 30

class ChatServer:

   def __init__(self, addr, file):

      self.host = addr[0]
      self.port = addr[1]
      self.socklist = []
      self.record = file
      self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.socklist.append(self.serversock)
      print("Socket created")

      try:
         self.serversock.bind( (self.host,self.port) )
      except socket.error as e:
         msg = "Failed at binding socket to [" + self.host + ":" + str(self.port) + "] address."
         msg += " Error number: " + str(e.errno) + ". Message: " + e.strerror + "\n"
         print(msg)
         self.record.close()
         sys.exit()

      print("Socket binded")

      self.serversock.listen(10)
      print("Server listening on port " + str(self.port) + "\n")
      self.record.write("<-- Session date: " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") +" -->\n\n" )

   def clientthread(self, conn):

      addr = conn.getpeername()
      self.socklist.append(conn)
      conn.settimeout(timeout)
      conn.sendall("Welcome to the server. Type something and hit enter\n".encode() )

      while True:

         try:

            data = conn.recv(1024)

         except socket.timeout as t:

            print("Timeout. ", end='' )
            self.record.write("Timeout. ")
            break

         if not data:
            break

         self.broadcast(data.decode(), conn)

      self.socklist.remove(conn)
      conn.sendall("Timeout. Connection lost with server\n".encode() )
      conn.close()
      print("Connection closed with [" + addr[0] + ":" + str(addr[1]) + "]\n" )
      self.record.write("Connection closed with [" + addr[0] + ":" + str(addr[1]) + "]\n")

   def broadcast(self, msg, sender):

      addr = sender.getpeername()
      fullmsg = "[" + addr[0] + ":" + str(addr[1]) + "] " + msg

      for sock in self.socklist:
         if sock != self.serversock and sock != sender:
            sock.sendall(fullmsg.encode() )

      print(fullmsg)
      self.record.write(fullmsg)

   def run(self):

      while True:

         conn, addr = self.serversock.accept()
         print("Connected with [" + addr[0] + ":" + str(addr[1]) + "]\n" )
         self.record.write("Connected with [" + addr[0] + ":" + str(addr[1]) + "]\n")

         threading.Thread(target=self.clientthread, args=(conn,) ).start()


def main():

   if len(sys.argv) != 3:
      print("Use: " + sys.argv[0] + " <IP> " + "<port>")
      sys.exit()

   ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

   if ip_pattern.search(sys.argv[1]) == None:
      print("Invalid IP address format")
      sys.exit()

   if sys.argv[2].isdigit() == False:
      print("Port must be a number (integer)")
      sys.exit()

   host = sys.argv[1]
   port = int(sys.argv[2])

   if (port >= 0 and port <= 65535) == False:
      print("Invalid port (must be 0-65535)") 
      sys.exit()

   file = open("record.log", "a")

   try:
      myServer = ChatServer( (host, port) , file)
      myServer.run()
   except KeyboardInterrupt:
      print()
   except Exception as e:
      print(e)

   file.write("\n<-- Session closed -->\n\n")
   file.close()

if __name__ == "__main__":
   main()

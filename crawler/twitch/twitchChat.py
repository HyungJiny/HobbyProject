# -*- coding: utf-8 -*-
from socket import *
from configparser import ConfigParser
import sys
import os, errno
import datetime
import time

# read config file
INIFILE = 'config.ini'
config = ConfigParser()
config.read(INIFILE)

# IRC chatserver info
server_name = 'irc.twitch.tv'
port = 6667
# password : oauth token
password = config.get('TWITCH', 'oauth_token')
# nick : twitch nickname
nickname = config.get('TWITCH', 'nickname')
# channel : # + streamer_id
channel = '#'
socket = socket(AF_INET, SOCK_STREAM)

def make_chatlog_file():
	'''
	make chatting log file
	if not exist directory then make it.
	file also too.
	return: opened file
	'''
	global channel

	today = datetime.date.today()
	dirpath = config.get('OUTPUT_FILE', 'twitch')
	filename = '{:%Y%m%d}_{channel}.csv'.format(today, channel=channel)

	if not os.path.exists(dirpath):
		os.makedirs(dirpath)
	if not os.path.exists(dirpath+'/'+filename):
		open_file = open(dirpath+'/'+filename, 'w', encoding='utf-8')
		open_file.write('time\tviewer_id\tmessage\n')
	else:
		open_file = open(dirpath+'/'+filename, 'a', encoding='utf-8')

	return open_file

def main(argv):
	global channel
	global socket
	log_number = 0

	if len(argv) < 2:
		print('python3 twitchChat.py <streamer_id>')
		sys.exit()
	channel += sys.argv[1]
	# Open file to store logs
	chatlog_file = make_chatlog_file()

	# Connect IRC chat
	socket.connect((server_name, port))
	socket.send(('PASS ' + password + '\r\n').encode())
	socket.send(('NICK ' + nickname + '\r\n').encode())
	socket.send(('JOIN '+channel + '\r\n').encode())

	# chatting crawling
	while True:
		try:
			recv_message = socket.recv(4096)
			# if chatting is stop
			#if len(recv_message) == 0: break
			# PING / PONG
			if recv_message == 'PING :tmi.twitch.tv\r\n' :
				socket.send('PONG :tmi.twitch.tv\r\n')
			else:
				# write logs
				# current epoch time
				current_time = str(int(time.time()))
				recv_message = recv_message.decode()
				print(recv_message)
				if 'PRIVMSG' in recv_message:
					message_split = recv_message.split(channel)
					viewer_id = message_split[0].split('!')[0][1:]
					message = str(message_split[-1][2:-1])
					chatlog_file.write(current_time+'\t'+viewer_id+'\t'+message+'\n')
		except KeyboardInterrupt:
			break

	chatlog_file.close()

if __name__ == "__main__":
	main(sys.argv)

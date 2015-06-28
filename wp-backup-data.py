#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from datetime import datetime
from argparse import ArgumentParser
from getpass import getpass
from sys import exit

def check_address(address):
	if not address or address.strip() == "":
		raise ValueError('address required')
	elif len(address) < 4:
		raise ValueError("address too short")

def check_username(username):
	if not username or username.strip() == "":
		raise ValueError('username required')
	elif len(username) < 4 or len(username) > 60:
		raise ValueError("username too short or too long")

def check_password(password):
	if not password or password.strip() == "":
		raise ValueError('password required')
	elif len(password) < 4:
		raise ValueError("password too short")

def check_field(checker, data):
	try:
		checker(data)
	except ValueError, e:
		print e
		exit(1)
	return data

def check_prompt_field(checker, field = "", password = False):
	while True:
		try:
			if password:
				data = getpass()
			else:
				data = raw_input(field)
			checker(data)
			break
		except ValueError, e:
			print e
			pass
	return data

ap = ArgumentParser(description="Do a backup of your WordPress data")
ap.add_argument("-u", "--user", help="username to use")
ap.add_argument("-p", "--password", help="password to use")
ap.add_argument("-P", "--prompt-for-password", dest="prompt_pwd", action="store_true", help="prompt for password to use")
ap.add_argument("-a", "--address", help="root address of the WordPress blog (example: 'blog.example.net')")
ap.add_argument("--http", dest="https", action="store_false", help="use HTTP as protocol")
ap.add_argument("--https", dest="https", action="store_true", help="use HTTPS as protocol (default)")
ap.set_defaults(https=True)
ap.set_defaults(prompt_pwd=False)
args = vars(ap.parse_args())

if not args["address"]:
	address = check_prompt_field(check_address, 'URL: ')
else:
	address = check_field(check_address, args["address"])

if not args["user"]:
	user = check_prompt_field(check_username, 'Username: ')
else:
	user = check_field(check_username, args["user"])

if args["prompt_pwd"] or not args["password"]:
	password = check_prompt_field(check_password, password = True)
else:
	password = check_field(check_password, args["password"])

if args["https"]:
	protocol = "https://"
else:
	protocol = "http://"

br = Browser()
br.set_handle_robots(False)

dt_format = "%Y-%m-%d_%H-%M-%S"
dt = datetime.today()
s = dt.strftime(dt_format)
filename = address + "_" + s + ".xml"

br.open(protocol + address + "/wp-login.php")
br.select_form(name="loginform")
br.form["log"] = user
br.form["pwd"] = password
br.submit()

br.open(protocol + address + "/wp-admin/export.php")
br.select_form(nr = 0)
backup = br.submit()

with open(filename, "w") as f:
	f.write(backup.read())

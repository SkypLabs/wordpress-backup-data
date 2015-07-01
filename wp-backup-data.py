#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from datetime import datetime
from argparse import ArgumentParser
from getpass import getpass
from sys import exit
from re import compile, IGNORECASE

def check_address(address):
	if not address or address.strip() == "":
		raise ValueError('address required')

	# These regex come from Django project
	# https://github.com/django/django/blob/master/django/core/validators.py
	ul = '\u00a1-\uffff'
	ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
	hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]*[a-z' + ul + r'0-9])?'
	domain_re = r'(?:\.[a-z' + ul + r'0-9]+(?:[a-z' + ul + r'0-9-]*[a-z' + ul + r'0-9]+)*)*'
	tld_re = r'\.[a-z' + ul + r']{2,}\.?'
	host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'
	regex = compile(
		r'(?:' + ipv4_re + '|' + host_re + ')'
		r'$', IGNORECASE
	)

	if not regex.match(address):
		raise ValueError('not a valid address')

def check_username(username):
	if not username or username.strip() == "":
		raise ValueError('username required')

def check_password(password):
	if not password or password.strip() == "":
		raise ValueError('password required')

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

ap = ArgumentParser(
		description="Do a backup of your WordPress data",
		epilog="Example: ./wp-backup-data.py -a blog.example.net -u user -P")
ap.add_argument("-u", "--user", help="username to use")
ap.add_argument("-p", "--password", help="password to use")
ap.add_argument("-P", "--prompt-for-password", dest="prompt_pwd", action="store_true", help="prompt for password to use")
ap.add_argument("-a", "--address", help="root address of the WordPress blog (examples: 'blog.example.net' or '192.168.20.53')")
ap.add_argument("--http", dest="https", action="store_false", help="use HTTP as protocol")
ap.add_argument("--https", dest="https", action="store_true", help="use HTTPS as protocol (default)")
ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.1.0")
ap.set_defaults(https=True)
ap.set_defaults(prompt_pwd=False)
args = vars(ap.parse_args())

try:
	if not args["address"]:
		address = check_prompt_field(check_address, 'Address: ')
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
except KeyboardInterrupt:
	print("\n\nGood Bye\n")
	exit(0)

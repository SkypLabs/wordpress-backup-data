#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from argparse import ArgumentParser, Action, ArgumentTypeError
from re import compile, IGNORECASE, MULTILINE
from datetime import datetime
from getpass import getpass
from os import access, W_OK
from os.path import isdir
from sys import exit

class check_dir(Action):
	def __call__(self, parser, namespace, values, option_string=None):
		directory = values
		if not isdir(directory):
			raise ArgumentTypeError("%s is not a valid path" % (directory))
		if access(directory, W_OK):
			setattr(namespace, self.dest, directory)
		else:
			raise ArgumentTypeError("%s is not a writable directory" % (directory))

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

if __name__ == "__main__":
	ap = ArgumentParser(
			description="Do a backup of your WordPress data",
			epilog="Example: ./wp-backup-data.py -a blog.example.net -u user -P")
	ap.add_argument("-u", "--user", help="username to use")
	ap.add_argument("-p", "--password", help="password to use")
	ap.add_argument("-P", "--prompt-for-password", dest="prompt_pwd", action="store_true", help="prompt for password to use")
	ap.add_argument("-a", "--address", help="root address of the WordPress blog (examples: 'blog.example.net' or '192.168.20.53')")
	ap.add_argument("-d", "--directory", action=check_dir, default=".", help="directory where the backup file will be stored")
	ap.add_argument("--http", dest="https", action="store_false", help="use HTTP as protocol")
	ap.add_argument("--https", dest="https", action="store_true", help="use HTTPS as protocol (default)")
	ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.2.0")
	ap.set_defaults(https=True)
	ap.set_defaults(prompt_pwd=False)

	try:
		args = vars(ap.parse_args())

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

		directory = args["directory"]

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

		doctype_re = compile("<\!DOCTYPE html>$", MULTILINE)
		result = backup.read()

		# If the result is a HTML document instead of a XML document
		if doctype_re.search(result):
			print("\nBad credentials\n")
			exit(1)

		with open(directory + "/" + filename, "w") as f:
			f.write(result)
	except KeyboardInterrupt:
		print("\n\nGood Bye\n")
		exit(0)
	except ArgumentTypeError as e:
		print "\n%s\n" % (e)
		exit(1)

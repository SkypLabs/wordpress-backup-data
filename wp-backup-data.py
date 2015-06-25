#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from datetime import datetime
from argparse import ArgumentParser
from getpass import getpass

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
	address = raw_input('URL: ')
else:
	address = args["address"]

if not args["user"]:
	user = raw_input('Username: ')
else:
	user = args["user"]

if args["prompt_pwd"]or not args["password"]:
	password = getpass()
else:
	password = args["password"]

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from datetime import datetime
from argparse import ArgumentParser

ap = ArgumentParser(description="Do a backup of your WordPress data")
ap.add_argument("-u", "--user", required = True, help = "username to use")
ap.add_argument("-p", "--password", required = True, help = "password to use")
ap.add_argument("-a", "--address", required = True, help = "root address of the WordPress blog (example: 'blog.example.net')")
ap.add_argument("--http", dest="https", action="store_false", help = "use HTTP as protocol")
ap.add_argument("--https", dest="https", action="store_true", help = "use HTTPS as protocol (default)")
ap.set_defaults(https=True)
args = vars(ap.parse_args())

br = Browser()
br.set_handle_robots(False)

dt_format = "%Y-%m-%d_%H-%M-%S"
dt = datetime.today()
s = dt.strftime(dt_format)
filename = args["address"] + "_" + s + ".xml"

if args["https"]:
	protocol = "https://"
else:
	protocol = "http://"

br.open(protocol + args["address"] + "/wp-login.php")
br.select_form(name="loginform")
br.form["log"] = args["user"]
br.form["pwd"] = args["password"]
br.submit()

br.open(protocol + args["address"] + "/wp-admin/export.php")
br.select_form(nr = 0)
backup = br.submit()

with open(filename, "w") as f:
	f.write(backup.read())

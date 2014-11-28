#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from datetime import datetime

class Protocol:
	http = "http://"
	https = "https://"

# --------------------

protocol = Protocol.https
fqdn = ""
username = ""
password = ""

# --------------------

br = Browser()
br.set_handle_robots(False)

dt_format = "%Y-%m-%d_%H-%M-%S"
dt = datetime.today()
s = dt.strftime(dt_format)
filename = fqdn + "_" + s + ".xml"

br.open(protocol + fqdn + "/wp-login.php")
br.select_form(name="loginform")
br.form["log"] = username
br.form["pwd"] = password
br.submit()

br.open(protocol + fqdn + "/wp-admin/export.php")
br.select_form(nr = 0)
backup = br.submit()

with open(filename, "w") as f:
	f.write(backup.read())

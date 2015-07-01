# WordPress Backup Config

This Python script is made for doing a complete backup of your Wordpress blog's data. It does exactly the same thing that the Wordpress' export feature.

## Dependancies

 * Python 2.7
 * [Mechanize][1] package

### On Fedora

	yum install python-mechanize

### On Debian

	aptitude install python-mechanize

### Using pip

	pip install mechanize

## How to

	usage: wp-backup-data.py [-h] [-u USER] [-p PASSWORD] [-P] [-a ADDRESS]
							 [--http] [--https] [-v]

	Do a backup of your WordPress data

	optional arguments:
	  -h, --help            show this help message and exit
	  -u USER, --user USER  username to use
	  -p PASSWORD, --password PASSWORD
							password to use
	  -P, --prompt-for-password
							prompt for password to use
	  -a ADDRESS, --address ADDRESS
							root address of the WordPress blog (examples:
							'blog.example.net' or '192.168.20.53')
	  --http                use HTTP as protocol
	  --https               use HTTPS as protocol (default)
	  -v, --version         show program's version number and exit

	Example: ./wp-backup-data.py -a blog.example.net -u user -P

## License

[GPL version 3][2]

  [1]: https://pypi.python.org/pypi/mechanize "Mechanize Python package"
  [2]: https://www.gnu.org/licenses/gpl.txt "GPL version 3"

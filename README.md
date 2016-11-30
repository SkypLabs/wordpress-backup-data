# WordPress Backup Config

This Python script is made for doing a complete backup of your Wordpress blog's data. It does exactly the same thing that the Wordpress' export feature.

## Dependencies

 * Python 2.7
 * [Mechanize][1] package

### On Fedora

	yum install python-mechanize

### On Debian

	aptitude install python-mechanize

### Using pip

	pip install mechanize

## How to

	usage: wp_backup_data.py [-h] [-u USER] [-p PASSWORD] [-P] [-O] [-a ADDRESS]
							 [-d DIRECTORY] [--http] [--https]
							 [--ignore-certificate] [-v]

	Do a backup of your WordPress data

	optional arguments:
	  -h, --help            show this help message and exit
	  -u USER, --user USER  username to use
	  -p PASSWORD, --password PASSWORD
							password to use
	  -P, --prompt-for-password
							prompt for password to use
	  -O, --prompt-for-otp  prompt for Yubikey OTP to use
	  -a ADDRESS, --address ADDRESS
							root address of the WordPress blog (examples:
							'blog.example.net' or '192.168.20.53')
	  -d DIRECTORY, --directory DIRECTORY
							directory where the backup file will be stored
	  --http                use HTTP as protocol
	  --https               use HTTPS as protocol (default)
	  --ignore-certificate  ignore invalid certificates
	  -v, --version         show program's version number and exit

	Example: ./wp-backup-data.py -a blog.example.net -u user -P

## Yubikey OTP support

If you have secured your Wordpress blog with the [Yubikey OTP plugin][2], the *-O* option is made for you ! By this way, you will be prompted to enter your OTP.

## With Docker

    docker run --rm -it -v <local path>:/backups docker.io/skyplabs/wordpress-backup-data

*local path* refers to the folder on your host system where the backup file will be stored.

If you want to store the backup file in your current directory :

    docker run --rm -it -v $(pwd):/backups docker.io/skyplabs/wordpress-backup-data

And if you want to specify some *options* :

    docker run --rm -it -v $(pwd):/backups docker.io/skyplabs/wordpress-backup-data -d /backups <options>

## License

[GPL version 3][3]

  [1]: https://pypi.python.org/pypi/mechanize "Mechanize Python package"
  [2]: https://wordpress.org/plugins/yubikey-plugin/ "Yubikey Wordpress plugin"
  [3]: https://www.gnu.org/licenses/gpl.txt "GPL version 3"

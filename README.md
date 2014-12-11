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

You have to complete these four parameters into the script :

    protocol = Protocol.https
    fqdn = ""
    username = ""
    password = ""

And to use it :

    ./wp-backup-data.py

## License

[GPL version 3][2]

  [1]: https://pypi.python.org/pypi/mechanize "Mechanize Python package"
  [2]: https://www.gnu.org/licenses/gpl.txt "GPL version 3"

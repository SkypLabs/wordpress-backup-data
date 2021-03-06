=====================
WordPress Backup Data
=====================

|PyPI Package| |Code Coverage| |Known Vulnerabilities|

This Python script is made for doing a complete backup of your WordPress
blog's data. It does the exact same job as the WordPress' export
feature.

This project is no more maintained.

Installation
============

With pip (recommanded)
----------------------

::

    pip install --upgrade wordpress-backup-data

From sources
------------

::

    git clone https://github.com/SkypLabs/wordpress-backup-data.git
    cd wordpress-backup-data
    python setup.py install

How to
======

::

    usage: wp-backup-data [-h] [-u USER] [-p PASSWORD] [-P] [-O] [-a ADDRESS]
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

    Example: ./wp-backup-data -a blog.example.net -u user -P

Yubikey OTP support
===================

If you have secured your WordPress blog with the `Yubikey OTP
plugin <https://wordpress.org/plugins/yubikey-plugin/>`__, the *-O*
option is made for you! By this way, you will be prompted to enter your
OTP.

With Docker
===========

::

    docker run --rm -it -v <local path>:/backups docker.io/skyplabs/wordpress-backup-data

*local path* refers to the folder on your host system where the backup
file will be stored.

If you want to store the backup file in your current directory:

::

    docker run --rm -it -v $(pwd):/backups docker.io/skyplabs/wordpress-backup-data

And if you want to specify some *options*:

::

    docker run --rm -it -v $(pwd):/backups docker.io/skyplabs/wordpress-backup-data -d /backups <options>

License
=======

`GPL version 3 <https://www.gnu.org/licenses/gpl.txt>`__

.. |Code Coverage| image:: https://api.codacy.com/project/badge/Grade/4e9d007ad30445e49137bef1c82c9b78
   :target: https://www.codacy.com/app/skyper/wordpress-backup-data?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SkypLabs/wordpress-backup-data&amp;utm_campaign=Badge_Grade
.. |Known Vulnerabilities| image:: https://snyk.io/test/github/SkypLabs/wordpress-backup-data/badge.svg
   :target: https://snyk.io/test/github/SkypLabs/wordpress-backup-data
.. |PyPI Package| image:: https://badge.fury.io/py/wordpress-backup-data.svg
   :target: https://badge.fury.io/py/wordpress-backup-data

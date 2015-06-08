distributed-duplicity
===================

Welcome to distributed-duplicity's GitHub repository. The repository contain a proof-of-concept prototype of a distributed backup system created as part of my master's thesis at [NTNU]. 

The backup system, named distributed-duplicity  use erasure codes and the backup software [Duplicity] to achieve increased availability and reliability through **encoding** and **distribution** of backup data.

The following open-source software needs to be installed to use distributed-duplicity:
* [Duplicity] - Encrypted bandwidth-efficient backup using the rsync algorithm.
* [zfec] - A fast erasure codec which can be used with the command-line, C, Python, or Haskell

Install [Duplicity]:
```sh
$ brew install duplicity
```
or
```sh
$ apt-get install duplicity
```
Install [zfec]:
```sh
$ pip install zfec
```

If installation of zfec fails, you might not have [python-dev] installed on your distribution:
```sh
$ apt-get install python-dev
```
Python-dev is required to compile certain python packages on pip. Installation of zfec will fail without it because it has some C files in need of compilation.

----------

[NTNU]:http://www.ntnu.no
[Duplicity]:http://duplicity.nongnu.org/
[zfec]:https://pypi.python.org/pypi/zfec
[GnuPG]:https://www.gnupg.org/


How does it work?
-------------
The software uses a coding technique called erasure coding to create redundancy data blocks. The software will identify any files in the backup source directory, and encode them into *n* partial files. Every storage host receives one partial file of each original file. In this prototype, the number of partial files and storage host should be equal.

The key to the solution is that only a subset of the partial files are required to restore the backup. That means that one, or more depending on configuration, may be down without disabling the possibility to restore the backup. This is also possible with simple data replication, but through the use of erasure codes, the storage overhead is significantly decreased.

The current version utilize [zfec], a Reed-Solomon based optimal erasure code library to create the partial files.

How to run a test of distributed-backup:
-------------

The configuration file (*duplicity_conf.py*) contains different variables for holding details about the storage hosts, and any options that should be passed to Duplicity. In general, notation from the [Duplicity] manual should be used. The default configuration is set up to the the backup locally to the local path "backup_test/". If you wish to perform a test with the default configuration, run the following command:
```sh
$ python distdup.py -k 2 -n 3 test/
```

The software will back up the test folder to the locla path "backup_test/". If you check the content of backup_test, you will see three folders, named distdup0, distdup1 and distdup2. Each folder correspond to one storage host. The folders contain [GnuPG] encrypted backup archives created by [Duplicity]. Distributed-duplicity is able to reconstruct the backup if 2/3 of the "storage hosts" is available at time of restoration.

If you wish to restore the backup, run the following command:
```sh
$ python distdup.py --restore restore_test/
```
The command will restore the backup according to the configuration file. In this case, it will restore it to the local path "restore_test/". This alone is not very interesting, and therefore the next step is to see if it is able to restore with one "storage host" unavailable. Delete the "backup_test/distdup0" directory, and try again:

```sh
rm -r restore_test/
rm -r backup_test/distdup0/
python distdup.py --restore restore_test/
```

This time, the software was able to restore with only 2 of the 3 storage hosts available. Through decoding the two partial parts Duplicity was able to restore, the original files was successfully reconstructed.


Feel free to test around with the xor and zfec encoder/decoder file to understand better how the erasure codes create partial files, and the content of the partial files.
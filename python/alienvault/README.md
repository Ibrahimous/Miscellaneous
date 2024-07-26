# Get the alienvault ip reputation data

Once upon a time there was a SOC analyst who looked for free IP reputation lists. Hereafter you may experiment part of his story.

## Check your installation

... by launching `check_install.sh` (you'll be asked for a password, your a sudoer, aren't you ?):
```
$ bash check_install.sh
```
        
## Download the feeds

... by launching `get_alienvault_feeds.py`
```
$ python get_alienvault_feeds.py
```

You should get the following output:
```
$ python get_alienvault_feeds.py 
Read config file successfully
Getting revision number...
Issuing get request to: https://reputation.alienvault.com/reputation.rev
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/connectionpool.py:734: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
  InsecureRequestWarning)
Get request successful
Got revision: 57682

Getting data...
Issuing get request to: https://reputation.alienvault.com/reputation.data
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/connectionpool.py:734: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
  InsecureRequestWarning)
Get request successful
Got data
Data written successfully to: feeds
```

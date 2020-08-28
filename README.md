# qBittorent rclone

This script helps you upload files downloaded by qBitorrent to Google Drive using Service accounts.

## How to use?
* Install [python](https://www.python.org/)
* Download [source code folder](https://github.com/Abu3safeer/qbittorrent_rclone/archive/master.zip).
* Rename folder to qbittorrent_rclone and copy it to your qBitorrent download folder.

![image](https://user-images.githubusercontent.com/12091003/91241948-c9f58e80-e74e-11ea-8b49-4bfd85018c19.png)
 
* folder path will be like this according to the example.

```
D:\Downloads\Torrent\qbittorrent_rclone
```

* Now go to Options => download  This check:
- [x] Run external program on torrent completion
* write this in the command field:
```
python "%D/qbittorrent_rclone/main.py" -t "%N" -c "%F" -r "%R" -s "%D"
```
![image](https://user-images.githubusercontent.com/12091003/91515996-1a0d5600-e8f3-11ea-85c8-79f8d4837491.png)

* Put your service accounts json files in accounts folder.
* Put Google Drive folder id in settings.ini file.
* Select what command used by rclone from ``move`` or ``copy`` or ``sync`` (Default is ``move``).
* Write rclone path (System PATH used by default)

You are ready to go.
# qBittorent rclone

This script helps you upload files downloaded by qBitorrent to Google Drive using Service accounts.

## How to use?
* Download [source code folder](https://github.com/Abu3safeer/qbittorrent_rclone/archive/master.zip) or [exe file from releases section](https://github.com/Abu3safeer/qbittorrent_rclone/releases).
* Copy qbittorrent_rclone folder to your qBitorrent download folder.

![image](https://user-images.githubusercontent.com/12091003/91241948-c9f58e80-e74e-11ea-8b49-4bfd85018c19.png)
 
* folder path will be like this according to the example.

```
D:\Downloads\Torrent\qbittorrent_rclone
```

* Now go to Options => download  This check:
- [x] Run external program on torrent completion
* write this in the command field:
```
python "%D/qbittorrent_rclone/[SCRIPT_FILE_NAME]" -t "%N" -c "%F" -r "%R" -s "%D"
```
* Replace [SCRIPT_FILE_NAME] with py file or exe file you downloaded.
* put your service accounts json files in accounts folder.
* put Google Drive folder id in settings.ini file.
* Select what command used by rclone (Default is move).
* Write rclone path (System PATH used by default)

You are ready to go.
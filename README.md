## Prerequisites

- Python3
- ffmpeg ([Download link](https://ffmpeg.org/download.html))
- Install the necessary Python packages by running: `pip install yt_dlp music-tag ytmusicapi Pillow requests`

### Note

`yt-dlp` should be installed by installing the python package, but if you find any trouble you can install it from its [GitHub link](https://github.com/yt-dlp/yt-dlp)

## How to use

Simply copy all the URLs or a search query of the videos/songs/albums/playlists you want to download in the file `to_download_urls_and_queries.txt` (one for each line). I recommend using YouTube Music (which allows for the official album covers to be downloaded with the proper resolution), but you can also use classic YouTube without issues (although some metadata might be missing).

Each entry in the `to_download_urls_and_queries.txt` must be either:
- A YouTube or YouTube Music URL.
- A formatted search query with the following format: `<artist>|<title of song/album/playlist>|<s/a/p (optional)>`, where `s/a/p` indicates whether you're searching for a **s**ong, **a**lbum or **p**laylist. If the last section is omitted, then the script will search for a song by default. For example, given the artist `Kanye West` and his album `Graduation`, in order to search for it you write the following entry in the file: `kanye west|graduation|a`. Queries are case insensitive.
- A free search query, but only if the option `--enable-free-search` has been passed. The query will be directly used as search cryteria on YouTube Music to choose the desired video/song/album/playlist.

Once the URLs and/or queries have been copied, simply launch the script:

```bash
python main.py
```

The script will create the downloaded `.mp3`s in the `downloads` directory where the script is located, although this can obviously be changed as you please by modifying the code or using the option `--destination-directory=<dest-directory/>`.

You can also launch the script with specific options as such:

```bash
python main.py --option1 --option2 ...
```

The possible options are the following:

- `--no-album`: if enabled the mp3 file will not have the artist's album in it.
- `--allow-playlist`: if enabled it allows to download the entire playlist from which the video is taken from. For example using this option in the following URL `https://music.youtube.com/watch?v=WwYbTxOZF0k&list=RDAMVMWwYbTxOZF0k` would download the entire playlist identified by the ID `RDAMVMWwYbTxOZF0k` specified in the query parameters of the URL.
- `--no-track-number`: if enabled the track number (if present) will not be written into the filename.
- `--playlists-in-their-own-directory`: if enabled the playlists will be placed in their own folder.
- `--no-log-files`: if enabled no log files will be produced during the execution.
- `--quiet-stdout`: if enabled the standard output to the command line will be minimized to the most important informations regarding the status of the execution.
- `--no-stdout`: if enabled no standard output will be produced. I do not recommend this as informations on the process are quite useful and I've spent a decent amount of time programming them.
- `--allow-non-squared-covers`: if enabled the research for the covers will also extend to non-squared images. If a non-squared image is used as cover either black bands will be present in it or the image will be cropped to a square.
- `--overwrite-files`: if enabled the destination files will be overwritten in case they already exist. If disabled (default behaviour) then the files will not be overwritten and the new file will be ending with ` (d)`, where `d` is a number representing the copy count.
- `--search-force-candidate-selection`: if enabled forces the selection to the best candidate while searching, ignoring any acceptance ratio set. This option can lead to some wrong downloads if not used with care.
- `--enable-free-search`: if enabled the script doesn't enforce a format for the search queries; instead it will directly search on YouTube Music the given query. It pretty much works as well as the given query.
- `--disabled-search-explicit-first`: if disabled the script won't try to find explicit songs first and will instead follow the natural order of the YouTube Music results.
- `--kbps=<kbps_value>`: Sets the kbps value to the one indicated in the command. Allowed values are: [96, 128, 160, 196, 228, 256, 288, 320].
- `--destination-directory=<dest-directory/>`: sets the destination directory, which is the directory where the files will be downloaded.
- `--cookies=<cookiefile>`: sets the cookiefile to be used to the given file. **This option may be necessary for explicit songs**.
- `--search-limit=<limit>`: sets the limit of entries to be searched. Must be a positive (not zero) integer.
- `--search-csv-delimiter=<delimiter>`: sets the CSV delimiter of the search strings format (for when free search is not used). Must be a single character.
- `--search-acceptance-ratio=<ratio>`: sets the ratio of string similarity accepted used in the searches. Must be a floating point value between the range $(0, 1]$. 
- `--general-acceptance-ratio=<ratio>`: sets the ratio of string similarity accepted used everywhere but in the searches. Must be a floating point value between the range $(0, 1]$. 

Every option that is not present in the previous list should be considered as an experimental option and not ready to be used.

For example, if you'd like a quiet execution with no log byproducts whatsoever or command line informations and audio quality set to 256 kbps, you could run the script as such:

```bash
python main.py --quiet-stdout --no-log-files --kbps=256
```

I usually run the following:

```bash
python main.py --overwrite-files --cookies=cookies.txt --playlists-in-their-own-directory --enable-free-search
```

If you'd like to modify options permanently, then modify the `options` JSON object inside `simox_yt2mp3_options.py`. There you'll find a couple more settings as well.

## Disclaimer

Use this script at your own risk regarding your YouTube account (whenever using cookies). I strongly recommend using a burner account.

## Accepted URLS format

All the URLS satisfying the following RegEX are accepted:

```
^http(s)?:\/\/(((www\.)?youtube|music\.youtube)\.com\/((watch\?v=[a-zA-Z0-9\-_]{11})(&list=[a-zA-Z0-9\-_]+)?|playlist\?list=[a-zA-Z0-9\-_]+)|youtu\.be\/[a-zA-Z0-9\-_]{11}(\?si=[a-zA-Z0-9\-_]+)?)$
```

Some examples:
- `https://music.youtube.com/watch?v=uG7eRgTwkck`
- `http://music.youtube.com/watch?v=uG7eRgTwkck`
- `https://www.youtube.com/watch?v=uG7eRgTwkck`
- `https://youtube.com/watch?v=PJ4JERVhYVQ&list=PLkq7KKY3sfbNLucY1orN0Bp2IYhCDSz25`
- `https://youtu.be/uG7eRgTwkck`
- `https://youtu.be/uG7eRgTwkck?si=NXiG6Z0zdnNIb6Kz`

If your URLs are not accepted, please try to clean them up or contact me to fix the RegEx.

## More on cookies

You can find some useful information to export cookies [here](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies).
Beware that Chromium-based browsers do not work for the cookies extraction through command line using `yt-dlp`.

Here's what I suggest:

1) Download Chrome if it isn't your preferred browser.
2) Install this [extension](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) to extract the cookies.
3) Login to YouTube in Chrome with a burner account (or at least I recommend using a burner, as you may get temporarily suspended for abusing downloads).
4) Export the cookies through the extension.
5) Paste the cookies in a chosen file (I recommend using a file "cookies.txt" in the same folder as the project).
6) When running the script pass the filename (with its path if it isn't in the same folder as the project) with the given option.

**REMEMBER NOT TO SHARE YOUR COOKIES** (unless you know what you're doing!)

## Feedback

If you encounter an error or think some functionalities could be added, please let me know by opening an issue on the [GitHub project](https://github.com/SimoxG7/youtube-to-mp3-with-tags)!
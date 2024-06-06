# JP-DATA

Flask webserver with a simple UI for managing kanji mnemonics and words.

## Features

* Supports multiple users
* Kanji information from [KANJIDIC](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project)
* Kanji decomposition data from [Kanji Database](https://kanji-database.sourceforge.net/)
* Remembering the Kanji keywords from [heisig-kanjis](https://github.com/sdcr/heisig-kanjis)
* Written in pure Python and Jinja2, no Javascript required!

## Screenshots

[<img src="screenshot_character.jpg" alt="screenshot character" width="512">](screenshot_character.jpg)
[<img src="screenshot_words.jpg" alt="screenshot_words" width="512">](screenshot_words.jpg)

## Installation

```bash
$ docker compose up --build -d
```

To initialize the database

```bash
$ docker exec -it jpdata-web-1 flask character insert
$ docker exec -it jpdata-web-1 flask decomp insert
$ docker exec -it jpdata-web-1 flask heisig insert
```

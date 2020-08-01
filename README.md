# Ultimate Installer

* [mpv](#mpv) - Command line video player
* [youtube-dl](#youtube-dl) - Command-line program to download videos from [YouTube](http://www.youtube.com) and other video sites
* [xampp](#xampp) - Most popular PHP development environment
* [git](#git) - Version control system
* [emacs](#emacs) - An extensible, customizable, free/libre text editor and more
* [xdman](#xdman) - XTREME download manager
* [chromium](#chromium) - Open-Source browser
* [feh](#feh) - Image viewer for Linux
* [go](#go) - go lang, open source programming language
* [atom](#atom) - A hackable text editor for the 21st Century
* [conda](#conda) - Anaconda is the birth place of python data science
* [geany](#geany) - lightweight programmer's text editor
* [audacity](#audacity) - Multi-track audio editor / recorder
* [ppsspp](#ppsspp) - PPSSPP is the PSP emulator for Android, Linux, Windows and more
* [heroku](#heroku) - Heroku command line software
* [kdenlive](#kdenlive) - Open-Source video editing software
* [mongodb](#mongodb) - Most popular database for modern apps.
* [node](#node) - JavaScript engine.
* [rvm](#rvm) - Ruby Version Manager
* [vysor](#vysor) - View and control your android on your computer.
* [postman](#postman) - Create and Test Your API's
* [robo3T](#robo3T) - MongoDB GUI
* [xclip](#xclip) - interact with clipboard through commandline.
* [ydl](#ydl) - easy youtube downloader
* [ytmpv](#ytmpv) - Play Youtube Videos in mpv player with custom quality
* [scrcpy](#scrcpy) - Display and Control your android
* [ghb](#handbrake_gui) - Video Converter
* [vbox](#vbox) - Virtual Box
* [openssh](#openssh) - connectivity tool for remote login with the SSH protocol
* [bittorrent](#bittorrent) - torrent Client
* [splay](#splay) - command line program to search and play songs
* [vmaster](#vmaster) - a quick hacky video manipulator command line script.

## [mpv](#mpv)
### Installation
```sh
sudo pacman -S mpv
```
### Uninstall
```sh
sudo pacman -R mpv && rm -rf "$HOME/.config/mpv"
```
### Enable some useful key bindings
```sh
curl 'https://pastebin.com/chsBd5s1' | grep -A 17 class=\"textarea\" | cut -d'>' -f2 | head -16 > "$HOME/.config/mpv/input.conf"
```
## [youtube-dl](#youtube-dl)
### Installation
```sh
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```
### Uninstall
```sh
sudo rm /usr/local/bin/youtube-dl
```

## [XAMPP](#xampp)
```sh
curl 'https://www.apachefriends.org/download.html' 2>/dev/null | grep '.run"' | cut -d\" -f8 | tail -1 | xargs wget && bash ./xampp*.run
```

# forg - file organizer
Python program for sorting files that have a YYYYmmdd date format at the beginning of their name.

This was made for a backup of my wifes old phones camera roll. All files here are named with the date and time they were taken. 

This program takes the date information and sorts the files into folders of `year/month/`. 

## Usage
**Basic usage**

`python forg.py path/to/source/dir/ path/to/output/dir/`

**Using locale settings for naming folders in your preffered language - danish for me**

`python forg.py --locale da_DK.UTF-8 path/to/source/dir/ path/to/output/dir/`

**Setting default locale, forg checks for default locale on every startup if not set with --locale**

`python forg.py --set-default-locale <locale-code>`

*Example:* `python forg.py --set-default-locale da_DK.UTF-8`

**Finding out what the default locale has been set to:**

`python forg.py --get-default-locale`
# forg - file organizer
Python program for sorting files that have a YYYYmmdd date format at the beginning of their name.

This was made for a backup of my wifes old phones camera roll. All files here are named with the date and time they were taken. 

This program takes the date information and sorts the files into folders of `year/month/`. 
## Requirement for use
The fundamental requirement for this program to function correctly is that the files to be read has the date format in the beginning of the file like so: **YYYYmmdd**. Example: **20190809_203700.jpg**. Here you can see that there is also a timestamp, but this is disregarded. The date at the beginning of the file tells the program that it was taken in 2019, on the 9th of August. This is the format that will ensure correct performance.

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
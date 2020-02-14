import argparse, sys, re, shutil, datetime, os, urllib, locale
from pathlib import Path
from time import sleep

class Forg:
    def __init__(self, source_dir, dest_dir):      
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)

        # Check to see if the directories exist
        if self.__source_directory_exists():

            # Firstly check to see if there is elgible files to move from source to destination folder
            if self.__inspect_source_directory():

                # Make sure the destination folder exists
                self.__prepare_destination_dir()


    def organize(self):
        translated = {}

        for file in self.files:
            filename = str(file).split('/')[-1][0:8]
            file_date = {'year': filename[0:4],
                         'month': filename[4:6]}
            
            # Change the month number to the month name
            file_date['month'] = datetime.date(int(file_date['year']), int(file_date['month']), 1).strftime('%B')

            # Construct the full path with the date
            dest_full_path = Path(self.dest_dir / file_date['year'] / file_date['month'].capitalize())

            # Check to see if it excists
            if not dest_full_path.exists():
                os.makedirs(dest_full_path)

            shutil.move(str(file), str(dest_full_path))


    def __inspect_source_directory(self):
        # Create a regex pattern to match the elgible files. 
        # We are going to match the whole path to the single files, so it takes that in account too
        pattern = re.compile('.+\d{8}.+')
        
        # List all files that have a date as the first thing in their filename
        files = [file for file in self.source_dir.glob('*') if pattern.match(str(file))]

        if not files:
            print("There were no elgible files to move in the source directory.", file=sys.stderr)
            exit(2)
        else:
            self.files = files
            return True


    def __source_directory_exists(self):
        if not self.source_dir.exists():
            print("The source directory does not exist - exiting program.", file=sys.stderr)
            exit(1)
        else:
            return True


    def __prepare_destination_dir(self):
        if not self.dest_dir.exists():
                os.makedirs(self.dest_dir)


if __name__ == '__main__':
    # Set up the parser. Require source and destination arguments
    parser = argparse.ArgumentParser(
        description='Put files in order by date, if the filename starts with a date '\
                    'of the format YYYYmmdd, like 20200101.'
    )
    parser.add_argument('source', help='Source directory for files to organize')
    parser.add_argument('destination', help='Destination directory for files to get organized in')
    parser.add_argument('-locale', dest='locale', help='Sets the locale for month names if system is not english.\n'\
                        'Remember that you need to pass the country code as well as the encoding, ex: da_DK.UTF-8')
    # Interpret the arguments passed to the script
    args = parser.parse_args()
    
    if args.locale:
        try:
            locale.setlocale(locale.LC_ALL, args.locale)
        except Exception as e:
            print("Something went wrong with assigning the custom locale.")
            print("Error message:\n", e)
    # Make sure the arguments are there, or else explain how the user needs to use the program
    if args.source and args.destination:
        
        # Create the organizer object
        forg_obj = Forg(
            source_dir=args.source,
            dest_dir=args.destination
        )

        # Organize!
        forg_obj.organize()
    else:
        print(args.usage)
        exit(1)
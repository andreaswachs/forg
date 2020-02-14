import argparse, sys, re, shutil, datetime, os, urllib, locale, shelve
from pathlib import Path
from tqdm import tqdm

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

        for file in tqdm(self.files, total=len(self.files), desc='Moving files', unit='file'):
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

    # This block is at the top because it needs to work beyond argparse
    # Handle single flag assignments, such as setting default settings
    if len(sys.argv) >= 2:
        # Open up the saved variables file
        forgdata = shelve.open('forgdata')

        # Handle the request of setting the default locale, if the user ran the program with this argument
        if sys.argv[1] == '--set-default-locale':
            
            # Make sure that there is the expected amount of arguments passed to the program.
            if len(sys.argv) == 3:
                forgdata['default-locale'] = sys.argv[2]
                print(f"Default locale set to {sys.argv[2]}. The program will now exit.")
            else:
                print("Illegal number of arguments passed. Expected flag and locale only.")

            forgdata.close()
            exit(0)

        # Handle asking for the default locale
        elif sys.argv[1] == '--get-default-locale':
            try:
                print(f"The default locale for this program is: {forgdata['default-locale']}.")
            except:
                print("There was no default locale set. You can set it with the flag --set-default-locale <locale-code>")

            forgdata.close()
            exit(0)

    # Set up the parser. Require source and destination arguments
    parser = argparse.ArgumentParser(
        description='Put files in order by date, if the filename starts with a date '\
                    'of the format YYYYmmdd, like 20200101.'
    )
    parser.add_argument('source', nargs=1, default=None, help='Source directory for files to organize.')
    parser.add_argument('destination', nargs=1, default=None, help='Destination directory for files to get organized in.')
    parser.add_argument('--locale', dest='locale', help='Sets the locale for month names if system is not english.\n'\
                        + 'Remember that you need to pass the country code as well as the encoding, ex: "da_DK.UTF-8".')
    parser.add_argument('--set-default-locale', dest="setdefaultlocale", help='Set the defautl locale so that you '\
                        + 'don\'t have to set the flag every time you use the program. If setting a default locale'\
                        + 'do put the flag first followed by the locale code and nothing else.')    
    parser.add_argument('--get-default-locale', dest='getdefaultlocale', help='Tells the user what the default locale is set to.')

    # Interpret the arguments passed to the script
    args = parser.parse_args()
    
    
    # Check to see if the forgdata shelve file exists, if so load the default locale
    try:
        forgdata = shelve.open('forgdata')
        if 'default-locale' in forgdata.keys():
            default_locale = forgdata['default-locale']
    except Exception as e:
        print(e)
        exit(1)

    if args.locale or default_locale:
        try:
            # Set a buffer to either assigned locale, from the save file or the args
            if args.locale:
                locale_buffer = args.locale
            elif default_locale:
                locale_buffer = default_locale

            locale.setlocale(locale.LC_ALL, locale_buffer)
        except Exception as e:
            print("Something went wrong with assigning the custom locale.")
            print("Error message:\n", e)
            print()
            
            print("Do you want to continue anyhow? Y/N")
            answer = input()
            if answer.lower() == 'n' and answer.lower() != 'y':
                exit(3)
            
                
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
        print(parser.usage)
        exit(1)
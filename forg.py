import argparse
import sys
from pathlib import Path

class Forg:
    def __init__(self, source_dir, dest_dir):      
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)

        # Check to see if the directories exist
        if self.__source_directory_exists():

            # Firstly check to see if there is elgible files to move from source to destination folder
            if self.__inspect_source_directory():

                # Make sure the destination folder exists
                # self.__prepare_destination_dir()
                print("We're ready to move files!")

    def organize(self):
        pass


    def __inspect_source_directory(self):
        # List all files that have a date as the first thing in their filename
        files = self.source_dir.glob('^\d{8}.+')

        if not files:
            print("There were no elgible files to move in the source directory.", file=sys.stderr)
            exit(2)
        else:
            return True


    def __source_directory_exists(self):
        if not self.source_dir.exists():
            print("The source directory does not exist - exiting program.", file=sys.stderr)
            exit(1)
        else:
            return True


    def __prepare_destination_dir(self):
        if not self.dest_dir.exists():
                self.dest_dir.mkdir()



if __name__ == '__main__':
    # Set up the parser. Require source and destination arguments
    parser = argparse.ArgumentParser(
        description='Put files in order by date, if the filename starts with a date '\
                    'of the format YYYYmmdd, like 20200101.'
    )
    parser.add_argument('source', help='Source directory for files to organize')
    parser.add_argument('destination', help='Destination directory for files to get organized in')
    
    # Interpret the arguments passed to the script
    args = parser.parse_args()
    
    # Make sure the arguments are there, or else explain how the user needs to use the program
    if args.source and args.destination:
        
        # Create the organizer object
        forg_obj = Forg(
            source_dir=arg.source,
            dest_dir=args.destination
        )

        forg_obj.organize()




    else:
        print(args.usage)
        exit(1)
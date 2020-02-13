import argparse

class Forg:

    def __init__(self):
        pass

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
        print("it works!")
    else:
        print(args.usage)
        exit(1)
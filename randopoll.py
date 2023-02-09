from argparse import ArgumentParser
from poller import Poller
from subprocess import run

parser = ArgumentParser(prog = "RandoPoll",
                    description = "What the program does")
parser.add_argument("filename")

args = parser.parse_args()

"""
Main Function to call on participants using Poller Class
And change participant data
"""
def main():
    with Poller(args.filename) as poller:
        for participant in poller:
            while True:
                print("%s: (A)nswered (C)orrect (E)xcused (M)issing (Q)uit" % participant)
                command = input().lower()
                if command == "a":
                    poller.attempted()
                    break
                elif command == "c":
                    poller.correct()
                    break
                elif command == "e":
                    poller.excused()
                    break
                elif command == "q":
                    poller.stop()
                    break
                elif command == "m":
                    poller.missing()
                    break
                print("Unknown response")         

if __name__ == "__main__":
    main()
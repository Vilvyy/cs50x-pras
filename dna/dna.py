import csv
import sys


def main():

    # Check if there are command line arguments
    if len(sys.argv) > 1:
        isFound = False
        # defining a dictionary called rows
        rows = []

    # TODO: Read database file into a variable
        # opening the first CLI Argument and storing them to a memory called database
        with open(sys.argv[1]) as database:
            # storing the value from the database to a variable called reader
            reader = csv.DictReader(database)
    # TODO: Read DNA sequence file into a variable
            # storing it to the rows dictionary
            for row in reader:
                rows.append(row)

    # TODO: Find longest match of each STR in DNA sequence
        with open(sys.argv[2]) as sequence:
            string = sequence.read()
        longest_AGATC = longest_match(string, "AGATC")
        longest_AATG = longest_match(string, "AATG")
        longest_TATC = longest_match(string, "TATC")

    # TODO: Check database for matching profiles
        for row in rows:
            if int(row["AGATC"]) == longest_AGATC and int(row["AATG"]) == longest_AATG and int(row["TATC"]) == longest_TATC:
                print(row["name"])
                isFound = True
                return row["name"]
    else:
        print("Invalid Arguments")
        return 1
    if isFound == False:
        print("No Match")
        return 1


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

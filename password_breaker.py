"""
Title: Chapter 15, Project 4, Automate the Boring Stuff
Purpose: Performs a dictionary attack on locked pdf files
Author: drstrangelove4
"""

import PyPDF2

DICT_PATH = "dictionary.txt"
PDF_LOCATION = "combinedminutes_encrypted.pdf"
NEW_PDF_NAME = "unencrypted_pdf.pdf"


# -----------------------------------------------------------------------------------------------------------------------


def load_dictionary(file_location):
    """
    Takes a path to a text file as an input and returns list of words(each line in the text file)
    with all whitespace removed. Import file should be a dictionary (as in oxford, not python data type).
    """
    word_dictionary = []

    # open the file at path
    with open(file_location) as file:
        # store the contents of the file in a variable
        file_contents = file.readlines()

        # Iterate through the file and append each line to a dict, strip the whitespace.
        for word in file_contents:
            word_dictionary.append(word.rstrip())

        return word_dictionary


# -----------------------------------------------------------------------------------------------------------------------


def load_file(pdf_location):
    # Open file
    print("Opening File:")

    try:
        # Attempt to load the file at the provided location
        pdf = open(pdf_location, "rb")
        encrypted_pdf_reader = PyPDF2.PdfReader(pdf)

    except Exception as err:
        return 0, err

    print("File Found.")
    return encrypted_pdf_reader, "nil"


# -----------------------------------------------------------------------------------------------------------------------


def attack_file(pdf_reader, word_dictionary):
    """
    Takes a pdf reader object and a dictionary of words as inputs and attempts to attack the password of the file.
    On success returns a decrypted reader object and a password.
    On failure returns code 0 and the encrypted reader object.
    """

    # Attempt to perform a dictionary attack on the password
    for x in range(len(word_dictionary)):
        print(f"Attempting password {x + 1} / {len(word_dictionary)}")
        try:
            # Call decrypt function
            pdf_reader.decrypt(word_dictionary[x].lower())
            # Attempt to open page - if this fails it will trigger an exception - if it passes then the return
            # statement will trigger.
            pdf_reader.pages[0]

            return word_dictionary[x].lower(), pdf_reader

        except Exception as _:
            # Nested another try/except block to use title case
            try:
                pdf_reader(word_dictionary[x].title())
                pdf_reader.pages[0]

                return word_dictionary[x].title(), pdf_reader

            except Exception as _:
                continue

    return 0, pdf_reader


# -----------------------------------------------------------------------------------------------------------------------


def make_unencrypted_file(pdf_reader_object):
    """
    Takes a pdf reader object as an input saves an unencrypted pdf file
    """
    print("Making unencrypted pdf.")
    pdf_writer = PyPDF2.PdfWriter()

    # Loop through the pages and add them to a writer object
    for x in range(len(pdf_reader_object.pages)):
        page_object = pdf_reader_object.pages[x]
        pdf_writer.add_page(page_object)

    # Save the file
    pdf_file = open(NEW_PDF_NAME, 'wb')
    pdf_writer.write(pdf_file)

    print("File saved.")


# -----------------------------------------------------------------------------------------------------------------------

def main():
    # Create a 'dictionary' list from a text file. This will be used to attack the password.
    word_dict = load_dictionary(DICT_PATH)

    # Load the pdf from path and error handling.
    encrypted_pdf, err = load_file(PDF_LOCATION)
    if isinstance(encrypted_pdf, int):
        raise Exception(f"There was an error opening the file: {err}")

    # Dictionary attack the file and error handling.
    password, pdf_reader_object = attack_file(encrypted_pdf, word_dict)
    if isinstance(password, int):
        raise Exception("Password has not been found")
    else:
        print(f"\nPassword found: {password}\n")

    # Create an unencrypted pdf
    if (input("Would you like to make an unencrypted version of the pdf? (yes/no) Default = no: ")).lower() == "yes":
        make_unencrypted_file(pdf_reader_object)

    print("Program exit")


# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

"""
Title: Chapter 15 Automate the Boring Stuff, Project 2 - Encrypting PDF's
Purpose: Starting from a specified root directory (default = cwd), this program will search for PDFs 
and encrypt all that it finds. It can also delete unencrypted PDF's if the user chooses to.
Author: drstrangelove4
"""


import os
from pprint import pprint
import PyPDF2
from send2trash import send2trash


ROOT_PATH = os.getcwd()  # Change to set path to find PDF's from.
FIND_TYPE = ".pdf"  # This program will not work with any other file types without rewriting get_pdf_paths().
PDF_SUFFIX = "_encrypted.pdf"
SPLIT_VALUE = "."
PASSWORD = "123"  # USE TO UNLOCK YOUR PDFS. CHANGE TO SOMETHING BETTER.
DELETE_OPTION = "yes"
DELETE_OPTION_2 = "y"
READ_MODE = "rb"
SAVE_MODE = "wb"
ENCRYPT_OPTION = "yes"
DELETE_FUNCTION_OPTION = 1


# ------------------------------------------------------------------------------------------------------------------------


def get_pdf_paths(root_path, find_type, new_suffix, split_value):
    """
    A function that takes no inputs and returns two lists of strings.
    The first is the file path and the second file names without the extension

    """
    pdf_paths = []
    pdf_new_paths = []

    # Scans each directory starting from the root path.
    for current_dir, _, files in os.walk(root_path):
        # Test each file to see if it is our desired filetype.
        for file in files:
            if find_type in file:
                # Create a path by joining the current directory with the file name.
                pdf_paths.append(os.path.join(current_dir, file))

                # Add the file name to the pdf names list.
                pdf_new_paths.append(
                    os.path.join(current_dir, (file.split(split_value)[0]) + new_suffix)
                )

    return pdf_paths, pdf_new_paths


# ------------------------------------------------------------------------------------------------------------------------


def create_pdfs(
    list_of_paths, list_of_new_paths, read_mode, save_mode, encrypt_option, password
):
    """
    Takes an input of 2 lists of file paths. The first being current file paths, the second being file paths after the function
    has encrypted the file.
    """
    for x in range(len(list_of_paths)):
        try:
            # Open each file in the path and create creater/writer objects
            working_pdf = open(list_of_paths[x], read_mode)
            reader = PyPDF2.PdfReader(working_pdf)

            # If the file is encrypted, attempt to decrypt it. Note this only works if all files are encrypted with the same password.
            if encrypt_option != "yes":
                reader.decrypt(password)
            writer = PyPDF2.PdfWriter()

            # Write each page in the file to the writer object.
            for i in range(len(reader.pages)):
                writer.add_page(reader.pages[i])

            # Encrypt the writer object to the password value in the constant above.
            if encrypt_option == "yes":
                writer.encrypt(password)

            # The next 2 lines are responsible for encrypting files, comment them out to disable encrypting files.
            new_pdf = open(list_of_new_paths[x], save_mode)
            writer.write(new_pdf)
            print(f"File saved to: {list_of_new_paths[x]}")

        except Exception as e:
            print(f"There was an error: {e}")


# ------------------------------------------------------------------------------------------------------------------------


def delete_pdfs(list_of_paths, pdf_suffix, option):
    """
    Takes an input of a list of file paths. Deletes all files in that list.
    """
    for pdf in list_of_paths:
        if option == 1:
            if pdf_suffix not in pdf:
                # Comment out next line to prevent program sending files to trash when this function runs.
                send2trash(pdf)
        else:
            if pdf_suffix in pdf:
                # Comment out next line to prevent program sending files to trash when this function runs.
                send2trash(pdf)

        print(f"File at: {pdf} has been sent to trash.")

    print("\nAll unencrypted pdf files have been removed.")


# ------------------------------------------------------------------------------------------------------------------------


def main():
    """
    Calls all other functions and passes relevant data to them. Handles user input.
    """
    # Call function to fill variables with paths
    pdf_path_list, new_paths = get_pdf_paths(
        root_path=ROOT_PATH,
        find_type=FIND_TYPE,
        new_suffix=PDF_SUFFIX,
        split_value=SPLIT_VALUE,
    )

    # Encrypt the pdfs in path.
    create_pdfs(
        list_of_paths=pdf_path_list,
        list_of_new_paths=new_paths,
        read_mode=READ_MODE,
        save_mode=SAVE_MODE,
        encrypt_option=ENCRYPT_OPTION,
        password=PASSWORD,
    )

    if pdf_path_list:
        # Give the user the choice to keep or remove unencrypted files.
        print(
            "\nWould you like to remove all unencrypted pdf files found at the following path(s)? "
        )

        # Print the list of files found in the path - ignore encrypted PDF's
        pprint([path for path in pdf_path_list if PDF_SUFFIX not in path])
        choice = input(
            "\nPress 'yes/y'to delete all, default option = keep files: "
        ).lower()

        # Based upon user choice, run the delete function.
        if choice == DELETE_OPTION or choice == DELETE_OPTION_2:
            delete_pdfs(
                list_of_paths=pdf_path_list,
                pdf_suffix=PDF_SUFFIX,
                option=DELETE_FUNCTION_OPTION,
            )
        else:
            print("Files have not been deleted")
    else:
        print(f"No pdf files found at {ROOT_PATH}")


# ------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

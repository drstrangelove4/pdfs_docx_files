import os
from pprint import pprint
from pdf_paranoia import get_pdf_paths, create_pdfs, delete_pdfs

ROOT_PATH = os.getcwd()
FIND_TYPE = "_encrypted.pdf"
NEW_SUFFIX = ".pdf"
SPLIT_VALUE = "_"
READ_MODE = "rb"
SAVE_MODE = "wb"
OPTION = "no"
PASSWORD = "123"
DELETE_OPTION = "yes"
DELETE_OPTION_2 = "y"
DELETE_FUNCTION_OPTION = 0

# ------------------------------------------------------------------------------------------------------------------------


def main():
    # Use the function from pdf_parranoia to get paths of encrypted PDFs and create new Paths for decrypted PDFs.
    pdf_path_list, new_paths = get_pdf_paths(
        root_path=ROOT_PATH,
        find_type=FIND_TYPE,
        new_suffix=NEW_SUFFIX,
        split_value=SPLIT_VALUE,
    )
    # Create the decrypted PDF's
    create_pdfs(
        list_of_paths=pdf_path_list,
        list_of_new_paths=new_paths,
        read_mode=READ_MODE,
        save_mode=SAVE_MODE,
        encrypt_option=OPTION,
        password=PASSWORD,
    )

    if pdf_path_list:
        # Give the user the choice to keep or remove unencrypted files.
        print(
            "\nWould you like to remove all unencrypted pdf files found at the following path(s)? "
        )

        # Print the list of files found in the path - ignore encrypted PDF's
        pprint([path for path in pdf_path_list if FIND_TYPE in path])

        # Take user input
        choice = input(
            "\nPress 'yes/y'to delete all, default option = keep files: "
        ).lower()

        # Based upon user input run the delete function.
        if choice == DELETE_OPTION or choice == DELETE_OPTION_2:
            delete_pdfs(
                list_of_paths=pdf_path_list,
                pdf_suffix=FIND_TYPE,
                option=DELETE_FUNCTION_OPTION,
            )
        else:
            print("Files have not been deleted")
    else:
        print(f"No pdf files found at {ROOT_PATH}")


# ------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

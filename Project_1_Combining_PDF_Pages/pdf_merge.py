"""
Title: Automate the Boring Stuff Chapter 15, Project 1
Purpose: Takes all the PFD files in the current working directory and merges them excluding the first page (unless length = 1 page)
Author: drstrangelove4
"""

import os
import PyPDF2
from datetime import datetime


# Constants to reduce magic value usage.
EXTENSION = ".pdf"
PAGE_SKIP = 0  # count starts from 0
SINGLE_PAGE = 1
NEW_PDF_NAME = f"{datetime.now().strftime('%d-%m-%Y--%H-%M')}-merged_PDF.pdf"
OPEN_MODE = "rb"
SAVE_MODE = "wb"


# ------------------------------------------------------------------------------------------------------------------------


def get_pdf_list():
    """
    Builds a list of pdfs in the cwd. Sorts them alphabetically and returns the list.
    """
    # Get the current working directroy
    files_in_directory = os.listdir(".")

    # Build and sort a list of pdf files found in the current working directroy
    pdfs_list = [file for file in files_in_directory if EXTENSION in file]
    pdfs_list.sort()

    return pdfs_list


# ------------------------------------------------------------------------------------------------------------------------


def add_pages(pdf_list):
    """
    Takes in a list of pdf locations and pulls the pages of each pdf into a central variable.
    """

    # Make a new variable that will store the pages of the pdf's passed to the function
    pdf_writer = PyPDF2.PdfWriter()

    for pdf_path in pdf_list:
        # open the current pdf and read the contents
        current_pdf = open(pdf_path, OPEN_MODE)
        pdf_reader = PyPDF2.PdfReader(current_pdf)

        # save the contents of each page skipping the first page unless the file is only a single page long.
        for x in range(len(pdf_reader.pages)):
            current_page = pdf_reader.pages[x]
            if x > PAGE_SKIP:
                pdf_writer.add_page(current_page)
            if len(pdf_reader.pages) == SINGLE_PAGE:
                pdf_writer.add_page(current_page)

    return pdf_writer


# ------------------------------------------------------------------------------------------------------------------------


def make_pdf(pdf_pages):
    """
    Writes the pages to a new file using a (mostly) unique name. Note if you run this more than once a per min it will overwrite
    the last PDF.
    """

    new_pdf = open(NEW_PDF_NAME, SAVE_MODE)
    pdf_pages.write(new_pdf)
    new_pdf.close()
    print("New PDF has been built")


# ------------------------------------------------------------------------------------------------------------------------


def main():
    """
    Main function. Responsible for calling all the functions and error handling in the case of not finding any pdf files.
    """
    pdf_path_list = get_pdf_list()
    if pdf_path_list:
        pdf_pages = add_pages(pdf_path_list)
        make_pdf(pdf_pages)
    else:
        raise Exception(
            "No .pdf files have been found in the current working directory."
        )


# ------------------------------------------------------------------------------------------------------------------------

main()

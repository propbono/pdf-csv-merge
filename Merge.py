#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import timeit

from Data import *
from Move import *


# in production add parameter "Working"
config = Configuration.factory()
cleaner = Move()
dict_data = ReturnData()


def merge_csv_from(pdf_list):

    data = Data(pdf_list)

    print("Creating CSV's:")
    data.save_all_csv()
    print("CSV - created!")

    print("Copying CSV's:")
    cleaner.move_merged_csv()
    print("CSV - copied!")


    print("Moving pdf's:")
    cleaner.rename_and_move_pdf(pdf_list)
    print("Pdf - moved!")

    return dict_data.files_added_to_csv, dict_data.files_skipped


if __name__ == "__main__":
    print("Creating pdf list:")
    pdf_list_tic = timeit.default_timer()
    pdf_list = [p for p in sorted(os.listdir(config.PREPPED_PDF_PATH)) if
                p.upper().startswith("U") and p.lower().endswith('.pdf')]
    pdf_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ",
          round(pdf_list_toc - pdf_list_tic, 4))
    files_to_process = len(pdf_list)
    print("Number of files to process", files_to_process)
    files_added_to_csv, files_skipped = merge_csv_from(pdf_list)
    print("Files added to csv: ", files_added_to_csv)
    print("Warning! Files was skipped: ", files_skipped)

    os.system("pause")


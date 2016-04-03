#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import timeit

from Data import *
from Move import *

class Merge():
    def __init__(self):
        self.config = Configuration.factory()
        self.pdf_list = self.__generate_pdf_list()

    def merge_csv_from(self):

        data = Data(self.pdf_list)
        cleaner = Move()
        dict_data = ReturnData()

        print("Creating CSV's:")
        dict_data = data.save_all_csv()
        print("CSV - created!")
        print()
        print("Copying CSV's:")
        cleaner.move_merged_csv()
        print("CSV - copied!")
        print()
        print("Moving pdf's:")
        cleaner.rename_and_move_pdf(self.pdf_list)
        print("Pdf - moved!")
        print()

        return dict_data.files_added_to_csv, dict_data.files_skipped

    def __generate_pdf_list(self):
        pdf_list = [p for p in sorted(os.listdir(self.config.PREPPED_PDF_PATH)) if
                    p.upper().startswith("U") and p.lower().endswith('.pdf')]
        return pdf_list

if __name__ == "__main__":
    print("Creating pdf list:")
    pdf_list_tic = timeit.default_timer()
    merge = Merge()
    pdf_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ",
          round(pdf_list_toc - pdf_list_tic, 4))
    print()
    files_to_process = len(merge.pdf_list)
    print("Number of files to process", files_to_process)
    files_added_to_csv, files_skipped = merge.merge_csv_from()
    print("Files added to csv: ", files_added_to_csv)
    print("Warning! Files was skipped: ", files_skipped)

    os.system("pause")


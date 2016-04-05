#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import timeit
import os
from Data import Data
from Move import Move
from Configuration import Configuration

class Merge(object):
    def __init__(self):
        self.config = Configuration.factory()
        self.pdf_list = self.__generate_pdf_list()

    def merge_csv_from(self):

        data = Data(self.pdf_list)
        cleaner = Move()

        print("Creating CSV's:")
        tic = timeit.default_timer()
        dict_data = data.save_all_csv()
        toc = timeit.default_timer()
        print("CSV - created!", "time (s): ", round(toc - tic, 4))
        print()
        print("Copying CSV's:")
        tic = timeit.default_timer()
        cleaner.move_merged_csv()
        toc = timeit.default_timer()
        print("CSV - copied!", round(toc - tic, 4))
        print()
        print("Moving pdf's:")
        tic = timeit.default_timer()
        pdf_to_remove = cleaner.rename_and_move_pdf(self.pdf_list)
        toc = timeit.default_timer()
        print("Pdf - moved!", round(toc - tic, 4))
        print()
        if pdf_to_remove is not None:
            print("There are some reprints - removing pdf")
            tic = timeit.default_timer()
            cleaner.delete_unused_pdf(pdf_to_remove)
            toc = timeit.default_timer()
            print("Reprint Pdf's removed", round(toc - tic, 4))
        return dict_data.files_added_to_csv, dict_data.files_skipped

    def __generate_pdf_list(self):
        pdf_list = [p for p in sorted(os.listdir(self.config.PREPPED_PDF_PATH)) if
                    p.upper().startswith("U") and p.lower().endswith('.pdf')]
        return pdf_list

if __name__ == "__main__":
    print("Creating pdf list:")
    tic = timeit.default_timer()
    merge = Merge()
    toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ", round(toc - tic, 4))
    print()
    files_to_process = len(merge.pdf_list)
    print("Number of files to process: ", files_to_process)
    files_added_to_csv, files_skipped = merge.merge_csv_from()
    print("Files added to csv: ", files_added_to_csv)
    if files_skipped > 0:
        print("Warning! There are unprepared files: ", files_skipped)

    os.system("pause")


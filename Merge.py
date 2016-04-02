#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import timeit
import csv

from DictionaryData import *
from Move import *


CSV_HEADERS_FLAT = ["comment", "Name", "Quantity", "Width", "Height",
                    "StockVendor", "StockName", "StockWeight", "IGNORED1",
                    "IGNORED2", "Priority", "TopOffcut", "LeftOffcut",
                    "BottomOffcut", "RightOffcut", "ProductID",
                    "Description", "Notes", "DueDate", "CompanyName",
                    "FirstName", "LastName", "ContentFile", "PageColor1",
                    "PageColor2", "ProductGroup", "Grain", "BleedsTop",
                    "BleedsLeft", "BleedsBottom", "BleedsRight",
                    "FolioSide1", "FolioSide2"]

CSV_HEADERS_BOUND_SELF = ["comment", "Name", "Quantity", "Width", "Height",
                          "StockVendor", "StockName", "StockWeight",
                          "IGNORED0", "TextPageCount", "LargestTextComponent",
                          "BindingMachine", "IGNORED1", "IGNORED2", "IGNORED3",
                          "ProductID", "Description", "Notes", "DueDate",
                          "CompanyName", "FirstName", "LastName",
                          "ContentFile", "IGNORED4", "INGORED5",
                          "PageColorName", "IGNORED6", "BleedsTop",
                          "BleedsLeft", "BleedsBottom", "BleedsRight",
                          "FolioPattern", "TextFolds", "IGNORED7",
                          "BindingNumberUp", "1stUpOrientation",
                          "NUpOrientation", "Grain"]

# in production add parameter "Working"
config = Configuration.factory()
clean = Move()
dict_data = Data()


def __save_csv_dict_data(key, data_dict, headers):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")  # date:
    # 2015-11-03T1935
    dir_name = os.path.join(config.MERGED_CSV_LOCAL, today)
    csv_file_name = os.path.join(config.MERGED_CSV_LOCAL, dir_name,
                                 key + '-' + now + '.csv')

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'a', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(data_dict)

def merge_csv_from(pdf_list):
    print("Collecting data to dictionary:")
    dict_tic = timeit.default_timer()

    data = DictionaryData(pdf_list)
    dict_data = data.add_data_to_dict()

    dict_toc = timeit.default_timer()
    print("All data in dictionary!", "time (s): ",
          round(dict_toc - dict_tic, 4))


    print("Creating CSV's:")
    csv_tic = timeit.default_timer()

    for key in dict_data.rows_flat.keys():
        __save_csv_dict_data(key, dict_data.rows_flat[key], CSV_HEADERS_FLAT)
    for key in dict_data.rows_bound.keys():
        __save_csv_dict_data(key, dict_data.rows_bound[key], CSV_HEADERS_BOUND_SELF)

    csv_toc = timeit.default_timer()
    print("CSV - created!", "time (s): ", round(csv_toc - csv_tic, 4))


    print("Copying CSV's:")
    copy_csv_tic = timeit.default_timer()

    clean.move_merged_csv()

    copy_csv_toc = timeit.default_timer()
    print("CSV - copied!", "time (s): ", round(copy_csv_toc - copy_csv_tic, 4))

    print("Moving pdf's:")
    move_pdf_tic = timeit.default_timer()

    clean.rename_and_move_pdf(pdf_list)

    move_pdf_toc = timeit.default_timer()
    print("Pdf - moved!", "time (s): ", round(move_pdf_toc - move_pdf_tic, 4))

    return dict_data.processed_files + dict_data.skipped_files


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
    processed_files = merge_csv_from(pdf_list)
    print("Number of files to process", files_to_process)
    print("Files processed: ", processed_files)

    os.system("pause")


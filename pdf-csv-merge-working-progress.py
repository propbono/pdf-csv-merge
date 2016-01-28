#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import _operator
import datetime

import os
import csv
import shutil
import timeit
import configuration

from Notes import *


CSV_HEADERS = ['NAME', 'KINDS', 'QUANTITY', 'WIDTH', 'HEIGHT', 'SIDE 1 COLORS',
               'SIDE 2 COLORS', 'CONTENT', 'PRODUCT GROUP', 'COMPANY',
               'FIRST NAME', 'FAMILY NAME', 'DESCRIPTION', 'NOTES', 'DUE DATE',
               'GRAIN', 'TOP OFFCUT', 'LEFT OFFCUT', 'BOTTOM OFFCUT',
               'RIGHT OFFCUT', 'PRIORITY']

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
                          "CompanyName", "First -> objectName", "LastName",
                          "ContentFile", "IGNORED4", "INGORED5",
                          "PageColorName", "IGNORED6", "BleedsTop",
                          "BleedsLeft", "BleedsBottom", "BleedsRight",
                          "FolioPattern", "TextFolds", "IGNORED7",
                          "BindingNumberUp", "1stUpOrientation",
                          "NUpOrientation", "Grain"]
# for future consideration
"""CSV_HEADERS_FOLDED = ["comment", "Name", "Quantity", "Width", "Height",
                      "StockVendor", "StockName", "StockWeight", "FoldCatalog",
                      "IGNORED", "Priority", "TopOffcut", "LeftOffcut",
                      "BottomOffcut", "RightOffcut", "Product MIS ID",
                      "Description", "Notes", "DueDate", "CompanyName",
                      "FirstName", "LastName", "ContentFile", "PageColor1",
                      "PageColor2", "ProductGroup", "Grain", "BleedsTop",
                      "BleedsLeft", "BleedsBottom", "BleedsRight",
                      "FolioPattern", "IGNORED", "CombinePages"]"""

ROWS_DICT_FLAT = {}
ROWS_DICT_BOUND = {}

# Change to config.Working in production
config = configuration.Debug


def _move_pdf_to_press_ready_pdf(name, new_name):
    shutil.move(os.path.join(config.PREPPED_PDF_PATH, name),
                os.path.join(config.PRESS_READY_PDF_PATH, new_name))

def _copy_pdf_to_done_folder(pdf):
    shutil.copyfile(os.path.join(config.PREPPED_PDF_PATH, pdf), os.path.join(
            config.PREPPED_PDF_DONE_PATH, pdf))

def rename_and_move_pdf(pdf_list):
    for i, pdf in enumerate(pdf_list, 1):
        new_pdf = Notes.delete_prepp_notes_from(pdf)
        _copy_pdf_to_done_folder(pdf)
        _move_pdf_to_press_ready_pdf(pdf, new_pdf)
        print(i, " *" * i)

def _merge_notes_for_without_csv(pdf, notes):
    if notes['type'] == "FLAT":

        row_flat = {"comment": "MetrixCSV2.0_FLAT", "Name": pdf[:-4],
                    "Quantity": notes["quantity"], "Width": notes["width"],
                    "Height": notes["height"], "StockVendor": "PG",
                    "StockName": notes["stockname"],
                    "StockWeight": notes["stockweight"], "IGNORED1": '',
                    "IGNORED2": '', "Priority": '5', "TopOffcut": '0',
                    "LeftOffcut": '0', "BottomOffcut": '0', "RightOffcut": '0',
                    "ProductID": '', "Description": pdf.split('-')[0],
                    "Notes": '', "DueDate": '', "CompanyName": pdf.split('-')[2],
                    "FirstName": '', "LastName": '', "ContentFile": '',
                    "PageColor1": '', "PageColor2": '',
                    "ProductGroup": ', "Grain":', "BleedsTop": '0.0625',
                    "BleedsLeft": '0.0625', "BleedsBottom": '0.0625', "BleedsRight": '0.0625',
                    "FolioSide1": "Front", "FolioSide2": "Back"}
        if "notes" in notes:
            row_flat["Notes"] = notes["notes"]
        row_flat["ContentFile"] = pdf
        if "group" in notes:
            row_flat["ProductGroup"] = notes["group"]


        return row_flat
    else:
        row_bound = {"comment": "MetrixCSV2.0_BOUND_SELF_COVER", "Name": pdf[:-4],
               "Quantity": notes["quantity"], "Width": notes["width"], "Height":
                   notes["height"], "StockVendor": "PG",
               "StockName": notes["stockname"], "StockWeight": notes["stockweight"],
                "IGNORED0": "", "TextPageCount": "", "LargestTextComponent": "4",
               "BindingMachine": "DUPLO", "IGNORED1": "", "IGNORED2": "",
               "IGNORED3": "", "ProductID": "", "Description": pdf.split('-')[
                0], "Notes": "",
               "DueDate": "", "CompanyName": pdf.split('-')[2], "FirstName": "",
               "LastName": "", "ContentFile": pdf, "IGNORED4": "",
               "INGORED5": "", "PageColorName": "Cyan, Magenta, Yellow, Black", "IGNORED6": "",
               "BleedsTop": "0.0625", "BleedsLeft": "0.0625", "BleedsBottom": "0.0625",
               "BleedsRight": "0.0625", "FolioPattern": "",
               "TextFolds": "",
               "IGNORED7": "", "BindingNumberUp": "", "1stUpOrientation": "HeadToJog",
               "NUpOrientation": "", "Grain": ""}

        if "pages" in notes:
            row_bound["TextPageCount"] = notes["pages"]
        row_bound["ProductID"] = ''  # pdf.split('-')[0] #this needs to be unique
        if "group" in notes:
            row_bound["Notes"] = notes["group"]
        if "notes" in notes:
            row_bound["Notes"] += " " + notes["notes"]



        return row_bound

def _add_data_to_dict(pdf_list):
    processed_files_with_name_change = 0
    processed_files_without_name_change = 0
    for pdf in pdf_list:
        try:
            pdf_without_notes, notes = Notes.extract_notes_from(pdf)
        except None:
            processed_files_without_name_change += 1
        else:
            # this method should be extracted to each product class and factory
            # method should decide which product is created
            data = _merge_notes_for_without_csv(pdf_without_notes, notes)
            key = notes["stock"]
            if notes["type"] == "FLAT":
                ROWS_DICT_FLAT.setdefault(key, []).append(data)
            else:
                ROWS_DICT_BOUND.setdefault(key,[]).append(data)
            print(pdf, " - added!")
            processed_files_with_name_change += 1
        finally:
            return processed_files_with_name_change, \
                   processed_files_without_name_change

def _save_csv_dict_data(key, data_dict,headers):
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

    processed_files_with_name_change, \
    processed_files_without_name_change = _add_data_to_dict(pdf_list)

    dict_toc = timeit.default_timer()
    print("All data in dictionary!", "time (s): ",
          round(dict_toc - dict_tic, 4))

    # _add_data_to_csv(pdf,notes) -crash here
    print("Creating CSV's:")
    csv_tic = timeit.default_timer()

    for key in ROWS_DICT_FLAT.keys():
        _save_csv_dict_data(key, ROWS_DICT_FLAT[key],CSV_HEADERS_FLAT)
    for key in ROWS_DICT_BOUND.keys():
        _save_csv_dict_data(key, ROWS_DICT_BOUND[key],CSV_HEADERS_BOUND_SELF)

    csv_toc = timeit.default_timer()
    print("CSV - created!", "time (s): ", round(csv_toc - csv_tic, 4))

    print("Copying CSV's:")
    copy_csv_tic = timeit.default_timer()

    move_merged_csv()

    copy_csv_toc = timeit.default_timer()
    print("CSV - copied!", "time (s): ", round(copy_csv_toc - copy_csv_tic, 4))

    print("Moving pdf's:")
    move_pdf_tic = timeit.default_timer()

    rename_and_move_pdf(pdf_list)

    move_pdf_toc = timeit.default_timer()
    print("Pdf - moved!", "time (s): ", round(move_pdf_toc - move_pdf_tic, 4))

    return processed_files_with_name_change + processed_files_without_name_change


def move_merged_csv():
    today = datetime.date.today().isoformat()
    remote_dir_name = os.path.join(config.MERGED_CSV_REMOTE, today)
    if not os.path.isdir(remote_dir_name):
        os.mkdir(remote_dir_name)
    local_csv_list = os.listdir(os.path.join(config.MERGED_CSV_LOCAL, today))
    for csv_name in local_csv_list:
        shutil.copy(os.path.join(config.MERGED_CSV_LOCAL, today, csv_name),
                    os.path.join(config.MERGED_CSV_REMOTE, today, csv_name))


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



# after creating all csv and copy them to NAS create project from merged csv
# move merged csv to done folder
# add names of csv to description of the

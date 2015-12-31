#!/usr/bin/python

# __author__ = 'propbono@gmail.com'
import _operator
import datetime

import os, sys, csv
import re
import shutil
import timeit
import configuration




CSV_HEADERS = ['NAME','KINDS','QUANTITY','WIDTH','HEIGHT','SIDE 1 COLORS','SIDE 2 COLORS','CONTENT','PRODUCT GROUP','COMPANY','FIRST NAME','FAMILY NAME','DESCRIPTION','NOTES','DUE DATE','GRAIN','TOP OFFCUT','LEFT OFFCUT','BOTTOM OFFCUT','RIGHT OFFCUT','PRIORITY']
ROWS_DICT = {}

# Change to config.Working in production
config = configuration.Debug


def _read_csv_values_for(pdf_name):
    #extract number from pdf name
    csv_name = _return_csv_name_for(pdf_name)
    csv_path_and_name= os.path.join(config.SOURCE_CSV_PATH, csv_name)
    with open(csv_path_and_name) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            return row

# Check what will happen if there will be no csv file for a pdf
def _return_csv_name_for(pdf_name):

    csv_list = sorted(os.listdir(config.SOURCE_CSV_PATH))
    for file in csv_list:
        if file.endswith('csv'):
            name = os.path.split(pdf_name)[1]
            pdf_name_number = name.split("-")[0]
            csv_file_number = os.path.split(file)[1]
            csv_file_number = csv_file_number.split("-")[0]
            if csv_file_number == pdf_name_number:
                return file

def _delete_prepp_notes_from(pdf):
    text_to_replace = _find_prepp_notes(pdf)
    if text_to_replace:
        return pdf.replace(text_to_replace[0], '')
    else:
        return pdf

def _move_pdf_to_press_ready_pdf(name, new_name):
   shutil.move(os.path.join(config.PREPPED_PDF_PATH, name),
               os.path.join(config.PRESS_READY_PDF_PATH, new_name))

# Add regular expressions to remove characters
def _find_prepp_notes(pdf):
    text_to_replace = re.findall(r'\(.*\)', pdf)
    if text_to_replace:
        return  text_to_replace
    else:
        return {}

def _parse_notes(notes):
    if notes["stock"] == "16pt":
       if int(notes["quantity"]) > 1000:
            notes["stock"] += "5000"
       else:
            notes["stock"] += "1000"


    if notes["group"] == "D":
        notes["group"] = "DIECUT"
    if notes["group"] == "O":
        notes["group"] = "ONESIDED"
    if notes["group"] == "S":
        notes["group"] = "SAMEDAY"
    if notes["group"] == "U":
        notes["group"] = "URGENT"
    if notes["group"] == "R":
        notes["group"] = "ROUNDCORNER"
    if notes["group"] == "P":
        notes["group"] = "PRESSSAMPLE"
    if notes["group"] == "M":
        notes["group"] = "MATTE"
    if notes["group"] == "N":
        notes["group"] = "NOAQ"

    if notes["group"] == "ONESIDED":
        notes["notes"] = notes["group"] + " " + notes["notes"]

    if notes["stock"] == "uv" or notes["stock"] == "u": # First save the current group to notes if exists then replace
        if notes["group"] != '':
            notes["notes"] += notes["group"] + " "
        notes["group"] = "UV"
    if notes["stock"] == "matte" or notes["stock"] == "m" :
        if notes["group"] != '':
            notes["notes"] += notes["group"] + " "
        notes["group"] = "MATTE"

    return notes

def _merge_notes_for_without_csv(pdf, notes):
    row = _read_csv_values_from_template()
    row['WIDTH'] = notes["width"]
    row['HEIGHT'] = notes["height"]
    if "group" in notes:
        row['PRODUCT GROUP'] = notes["group"]
    if "notes" in notes:
        row['NOTES']= notes["notes"]
    row['QUANTITY'] = notes["quantity"]
    row['CONTENT'] = pdf
    row['NAME'] =  pdf[:-4]
    row['DESCRIPTION'] = pdf.split('-')[0]
    return row

def extract_notes_from(pdf):
# SampleName(3.5x2-16pt1000-g:sameday-n:diecut PocketFolder 4 inch)-1000.pdf
    notes = {'width':'', 'height':'',"stock":'','quantity':'','notes':'','group':''}
    notes_from_pdf = _find_prepp_notes(pdf)
    if notes_from_pdf:
        notes_from_pdf = notes_from_pdf[0].lstrip('(').rstrip(')').split('-')
        notes["width"] = notes_from_pdf[0].split('x')[0]
        notes["height"] = notes_from_pdf[0].split('x')[1]
        notes["stock"] = notes_from_pdf[1].lower()
        notes["quantity"] = pdf.split('-')[-1].rstrip(".pdf")

        for n in notes_from_pdf[2:]:
            if _operator.contains(n,"n;"):
                notes["notes"] = n.lstrip("n;")
            elif _operator.contains(n,"g;"):
                notes["group"] = n.lstrip("g;").upper()

    if notes['width'] != '':
        notes = _parse_notes(notes)
        pdf = _delete_prepp_notes_from(pdf)
        return pdf, notes
    else:
        return pdf, None

def _copy_pdf_to_done_folder(pdf):
    shutil.copyfile(os.path.join(config.PREPPED_PDF_PATH, pdf), os.path.join(
                                 config.PREPPED_PDF_DONE_PATH, pdf))

def rename_and_move_pdf(pdf_list):
    for i, pdf in enumerate(pdf_list, 1):
        new_pdf = _delete_prepp_notes_from(pdf)
        _copy_pdf_to_done_folder(pdf)
        _move_pdf_to_press_ready_pdf(pdf, new_pdf)
        print(i, " *"*i)

def _add_data_to_dict(pdf_list):
    processed_files_with_name_change = 0
    processed_files_without_name_change = 0
    for pdf in pdf_list:
        pdf_without_notes, notes = extract_notes_from(pdf)
        if notes is not None:
            data = _merge_notes_for_without_csv(pdf, notes)
            key = notes["stock"]
            ROWS_DICT.setdefault(key, []).append(data)
            print(pdf, " - added!")
            processed_files_with_name_change += 1
        else:
            processed_files_without_name_change += 1
    return processed_files_with_name_change, processed_files_without_name_change

def _save_csv_dict_data(key, data_dict):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")  # date:
    # 2015-11-03T1935
    dir_name = os.path.join(config.MERGED_CSV_LOCAL, today)
    csv_file_name = os.path.join(config.MERGED_CSV_LOCAL, dir_name, key + '-' + now
                                 + '.csv')

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'a', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = CSV_HEADERS)
            writer.writeheader()
            writer.writerows(data_dict)

def merge_csv_from(pdf_list):
    print("Collecting data to dictionary:")
    dict_tic = timeit.default_timer()

    processed_files_with_name_change, processed_files_without_name_change =\
        _add_data_to_dict(pdf_list)

    dict_toc = timeit.default_timer()
    print("All data in dictionary!", "time (s): ",round(dict_toc - dict_tic, 4))

    #_add_data_to_csv(pdf,notes) -crash here
    print("Creating CSV's:")
    csv_tic = timeit.default_timer()

    for key in ROWS_DICT.keys():
        _save_csv_dict_data(key, ROWS_DICT[key])

    csv_toc = timeit.default_timer()
    print("CSV - created!","time (s): ", round(csv_toc-csv_tic,4))

    print("Copying CSV's:")
    copy_csv_tic = timeit.default_timer()

    move_merged_csv()

    copy_csv_toc = timeit.default_timer()
    print("CSV - copied!","time (s): ", round(copy_csv_toc-copy_csv_tic,4))

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

# temp function we can eliminate this if we declare the dictionary with proper columns
def _read_csv_values_from_template():
    #extract number from pdf name
    csv_path_and_name= os.path.join(DIR,"csv_template.csv")
    with open(csv_path_and_name) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            return row

if __name__ == "__main__":
    print("Creating pdf list:")
    pdf_list_tic = timeit.default_timer()
    pdf_list = [p for p in sorted(os.listdir(config.PREPPED_PDF_PATH)) if
                p.upper().startswith("U") and p.lower().endswith('.pdf')]
    pdf_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ", round(pdf_list_toc -  pdf_list_tic,4))
    files_to_process = len(pdf_list)
    print("Number of files to process", files_to_process)
    processed_files = merge_csv_from(pdf_list)
    print("Number of files to process", files_to_process)
    print("Files processed: ", processed_files)

    os.system("pause")


# rid off csv completly and check processing time


# after creating all csv and copy them to NAS create project from merged csv
# move merged csv to done folder
# add names of csv to description of the


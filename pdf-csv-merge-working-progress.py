#!/usr/bin/python

# __author__ = 'propbono'
import _operator
import datetime

import os, sys, csv
import re
import shutil


CSV_HEADERS = ['NAME','KINDS','QUANTITY','WIDTH','HEIGHT','SIDE 1 COLORS','SIDE 2 COLORS','CONTENT','PRODUCT GROUP','COMPANY','FIRST NAME','FAMILY NAME','DESCRIPTION','NOTES','DUE DATE','GRAIN','TOP OFFCUT','LEFT OFFCUT','BOTTOM OFFCUT','RIGHT OFFCUT','PRIORITY']


# First check what pdf files we have in the folder
DIR = os.path.dirname(sys.argv[0])

PREPPED_PDF_PATH = "N:\\"
PRESS_READY_PDF_PATH = "Q:\\"
SOURCE_CSV_PATH = "O:\\"
MERGED_CSV_REMOTE = "K:\\"
PREPPED_PDF_DONE_PATH = os.path.join(PREPPED_PDF_PATH,"00Done")
MERGED_CSV_LOCAL = os.path.join(DIR,"merged_csv")

def _read_csv_values_for(pdf_name):
    #extract number from pdf name
    csv_name = _return_csv_name_for(pdf_name)
    csv_path_and_name= os.path.join(SOURCE_CSV_PATH,csv_name)
    with open(csv_path_and_name) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            return row

# Check what will happen if there will be no csv file for a pdf
def _return_csv_name_for(pdf_name):

    csv_list = sorted(os.listdir(SOURCE_CSV_PATH))
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
    newpdf = pdf.replace(text_to_replace[0], '')
    return newpdf

def _move_pdf_to_press_ready_pdf(name, new_name):
   shutil.move(os.path.join(PREPPED_PDF_PATH, name),
                os.path.join(PRESS_READY_PDF_PATH,new_name))

# Add regular expressions to remove characters
def _find_prepp_notes(pdf):
    text_to_replace = re.findall(r'\(.*\)', pdf)
    if text_to_replace:
        return  text_to_replace
    else:
        return {}

def _merge_notes_for(pdf, notes):
    row = _read_csv_values_for(pdf)
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
    notes = {}
    notes_from_pdf = _find_prepp_notes(pdf)
    if notes_from_pdf:
        notes_from_pdf = notes_from_pdf[0].lstrip('(').rstrip(')').split('-')
        notes["width"] = notes_from_pdf[0].split('x')[0]
        notes["height"] = notes_from_pdf[0].split('x')[1]
        notes["stock"] = notes_from_pdf[1].lower()
        notes["quantity"] = pdf.split('-')[-1].rstrip(".pdf")

        if notes["stock"] == "16pt":
            if int(notes["quantity"]) > 1000:
                notes["stock"] += "5000"
            else:
                notes["stock"] += "1000"

        for n in notes_from_pdf[2:]:
            if _operator.contains(n,"n;"):
                notes["notes"] = n.lstrip("n;")
            elif _operator.contains(n,"g;"):
                notes["group"] = n.lstrip("g;").upper()

        return notes
    else:
        return None

def _save_csv_data(dir_name, pdf, notes):
    today = datetime.date.today().isoformat()
    csv_file_name = os.path.join(MERGED_CSV_LOCAL,dir_name,
                                 notes["stock"]+'-'+today+'-V1'+'.csv')

    fieldnames = CSV_HEADERS
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writeheader()
            row = _merge_notes_for(pdf, notes)
            writer.writerow(row)
            print("saved")
    else:
        with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            row = _merge_notes_for(pdf, notes)
            writer.writerow(row)
            print("saved")

def _copy_pdf_to_done_folder(pdf):
    shutil.copyfile(os.path.join(PREPPED_PDF_PATH, pdf), os.path.join(
                                 PREPPED_PDF_DONE_PATH, pdf))

def rename_and_move(pdf):
    new_pdf = _delete_prepp_notes_from(pdf)
    _copy_pdf_to_done_folder(pdf)
    _move_pdf_to_press_ready_pdf(pdf, new_pdf)
    return new_pdf

def add_data_to_csv(pdf, notes):
    today = datetime.date.today().isoformat()
    dir_name = os.path.join(MERGED_CSV_LOCAL,today)
    if os.path.isdir(dir_name):
        print("Directory exists - saving file: ", pdf)
        _save_csv_data(dir_name, pdf, notes)
    else:
        print("Directory doesn't exists - creating directory: ", dir_name)
        os.mkdir(dir_name)
        print("Saving file: ", pdf)
        _save_csv_data(dir_name, pdf, notes)

def merge_csv_from(pdf_list):
    processed_files_count = 0

    for pdf in pdf_list:
        notes = extract_notes_from(pdf)
        if notes is not None:
            pdf = rename_and_move(pdf)
            add_data_to_csv(pdf,notes)
            processed_files_count += 1
        else:
            _copy_pdf_to_done_folder(pdf)
            _move_pdf_to_press_ready_pdf(pdf,pdf)
            print("Not in csv's - moving file: ", pdf)
    # global dictionary_of_all_list
    # for pdf in pdf_list:
    #   notes = extract_notes_from(pdf)
    #   if notes is not None:
    #       dictionary_of_all_list = add_data_to_dictionary(pdf, notes)
    #       files_in_csv_count += 1 - change this to counting in specific list, actually I think it's enough to return list size.
    #   else:
    #        _copy_pdf_to_done_folder(pdf)
    #       _move_pdf_to_press_ready_pdf(pdf,pdf)
    #       print("Not in csv's - moving file: ", pdf)
    #for dictionary in dictionary_of_allList:
    #    _save_csv_data(dictionary) - change _save_csv_data() function to check if the name of csv exists and if so create different one
    #                                 open csv file once and save in the loop all the files in the list to this file.
    #

    return processed_files_count

def move_merged_csv():
    today = datetime.date.today().isoformat()
    remote_dir_name = os.path.join(MERGED_CSV_REMOTE,today)
    if not os.path.isdir(remote_dir_name):
        os.mkdir(remote_dir_name)
    remote_csv_list = os.listdir(remote_dir_name)
    local_csv_list = os.listdir(os.path.join(MERGED_CSV_LOCAL,today))
    for merged_csvs in local_csv_list:
        move_csv_file_recursion(merged_csvs,remote_csv_list)

def move_csv_file_recursion(name, list):
    if name in list:
        i = name[-5:-4]
        n = name[:-5] + str(int(i)+1)+".csv"
        _move_pdf_merged_csv(name,n)
    else:
        _move_pdf_merged_csv(name, name)

def _move_pdf_merged_csv(name, new_name):
     today = datetime.date.today().isoformat()
     shutil.copy(os.path.join(MERGED_CSV_LOCAL,today, name),
                os.path.join(MERGED_CSV_REMOTE,today,new_name))


if __name__ == "__main__":
    pdf_list = [p for p in sorted(os.listdir(PREPPED_PDF_PATH)) if
                p.startswith("U") and p.endswith('.pdf')]

    files_to_process = len(pdf_list)
    print("Number of files to process", files_to_process)
    proccessed_files = merge_csv_from(pdf_list)
    print("Number of files to process", files_to_process)
    print("Files proccessed: ", proccessed_files)
    # repair this function
    # move_merged_csv()

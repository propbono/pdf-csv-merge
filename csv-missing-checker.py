import datetime


__author__ = 'prepress'
import csv, os, sys
import timeit
from Status import status
from collections import defaultdict

DIR = os.path.dirname(sys.argv[0])

NEW_UPLOADS_PATH = os.path.join(DIR,"00New")
PREPPED_UPLOADS_PATH = os.path.join(DIR,"00Prepped")
INAPROVAL_UPLOADS_PATH = os.path.join(DIR,"00InApproval")
ONHOLD_UPLOADS_PATH = os.path.join(DIR,"00OnHold")
CANCELLED_UPLOADS_PATH = os.path.join(DIR,"00Cancelled")
PRESSREADY_UPLOADS_PATH = os.path.join(DIR,"00PressReady")
DONE_UPLOADS_PATH = os.path.join(DIR,"00Done")
SIGNS_UPLOADS_PATH = os.path.join(DIR,"00Signs")
DIGITAL_UPLOADS_PATH = os.path.join(DIR,"00Digital")
OUTSOURCED_UPLOADS_PATH = os.path.join(DIR,"00Outsourced")

# PREPPED_PDF_PATH = "N:\\"
# PRESS_READY_PDF_PATH = "Q:\\"
# SOURCE_CSV_PATH =  #"O:\\"
# MERGED_CSV_REMOTE = "K:\\"
# PREPPED_PDF_DONE_PATH = os.path.join(PREPPED_PDF_PATH,"00Done")
# MERGED_CSV_LOCAL = os.path.join(DIR,"merged_csv")

CSV_HEADERS = ['Upload', 'Status', 'Date', 'Run']

CSV_DICT = {}
CSV_LIST = []


def save_initial_data_to_csv(name):

    print("Creating csv list:")
    csv_list_tic = timeit.default_timer()

    all_uploads_list = return_all_upload_numbers()

    csv_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ", round(csv_list_toc - csv_list_tic, 4))
    print()


    print("Creating csv db:")
    csv_db_tic = timeit.default_timer()

    with open(name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for element in all_uploads_list:
            row = {CSV_HEADERS[0]: element, CSV_HEADERS[1]: status.New,
                   CSV_HEADERS[2]: datetime.date.today(),CSV_HEADERS[3]: None }
            writer.writerow(row)

    csv_db_toc = timeit.default_timer()
    print("CSV db - created!", "time (s): ", round(csv_db_toc - csv_db_tic, 4))


# I think I can create dictionary here and have only one loop over the csv's
def return_all_upload_numbers():
    orders_list = [c.split("-")[0] for c in sorted(os.listdir(NEW_UPLOADS_PATH)) if
                c.lower().endswith('.csv')]
    return orders_list

# returns current db structure
def return_current_db():
    columns = defaultdict(list)
    with open("csv_missing_db.csv") as csv_db:
        reader = csv.DictReader(csv_db)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)
    return columns

def list_of_new_uploads():
    all_uploads_list = return_all_upload_numbers()
    uploads_in_database = return_current_db()[0] # column with uploads
    return list(set(all_uploads_list) - set(uploads_in_database))

def list_of_prepped_uploads():
    pass

def list_of_inapproval_uploads():
    pass

def list_of_onhold_uploads():
    pass

def list_of_cancelled_uploads():
    pass

def list_of_press_ready_pdfs():
    pdf_list = [p.split("-")[0] for p in sorted(os.listdir(PRESS_READY_PDF_PATH)) if
                p.lower().endswith('.pdf') and p.lower().startswith('U') ]
    return pdf_list

def list_of_done_uploads():
    pass

def list_of_signs_uploads():
    pass

def list_of_digital_uploads():
    pass

def list_of_outsourced_uploads():
    pass


def update_db(name):
    db_status = ""
    all_orders = return_all_upload_numbers()
    orders_in_db = #grab orders from csv_db
    press_ready_pdfs = list_of_press_ready_pdfs()

    current_orders = list(set(all_orders)-set(orders_in_db))

    for o in current_orders:
        if o in press_ready_pdfs:
            db_status = status.Done
        elif o in waiting_pdfs:
            db_status = status.InApproval
        else:
            db_status = ""

    # loook at current list and make set with the all csv files
    # then for all set check
    with open(csv_file_name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        save_rows_to_csv(csv_list, writer, db_status)

if __name__ == "__main__":

    name = "csv_missing_db.csv"
    if not os.path.exists(name):
        save_initial_data_to_csv(name)
    else:
        update_db(name)


# Procedure
# 0. Add initial data to database:
#       a - set all status as new
#       b - check waiting folder and set status inapproval for all order there
#       c - check onhold folder and set status on hold for all order there
#       d - check cancelled folder and set status on hold
#       c - check folder signs and digital and set proper status
#       d -
# 1. Add new orders to top of the list (for current day) if its not on the
# list already                  - New           - Date
# 2. Check and modify status of all jobs:
        # a - waiting directory - InApproval    - Date
        # b - cancel directory  - Cancelled     - Date
        # c - done directory    - Prepped       - Date
        # d - on hold directory - OnHold        - Date
        # e - pressready dir    - PressReady    - Date
        # f - gagn run dir      - Done          - Date  - PGW, PGW
        # g - outsource folder  - Outsourced    - Date
        # h - signs dir         - Signs         - Date
        # i - digital dir       - Digital       - Date
# 3. Modify stastus for jobs what changed
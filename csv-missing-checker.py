__author__ = 'prepress'
import csv, os, sys
import timeit

DIR = os.path.dirname(sys.argv[0])
PREPPED_PDF_PATH = "N:\\"
PRESS_READY_PDF_PATH = "Q:\\"
SOURCE_CSV_PATH = "O:\\"
MERGED_CSV_REMOTE = "K:\\"
PREPPED_PDF_DONE_PATH = os.path.join(PREPPED_PDF_PATH,"00Done")
MERGED_CSV_LOCAL = os.path.join(DIR,"merged_csv")
CSV_HEADERS = ['Upload', 'Status']

CSV_DICT = {}
CSV_LIST = []


def save_initial_data_to_csv(name):

    print("Creating csv list:")
    csv_list_tic = timeit.default_timer()

    orders_list = list_of_csv_files()

    csv_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ", round(csv_list_toc - csv_list_tic, 4))
    print()

    print("Creating csv db:")
    csv_db_tic = timeit.default_timer()

    with open(name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        save_rows_to_csv(orders_list, writer, "done")

    csv_db_toc = timeit.default_timer()
    print("CSV db - created!", "time (s): ", round(csv_db_toc - csv_db_tic, 4))


def list_of_csv_files():
    orders_list = [c.split("-")[0] for c in sorted(os.listdir(SOURCE_CSV_PATH)) if
                c.lower().endswith('.csv')]
    return orders_list

def list_of_press_ready_pdfs():
    pdf_list = [p.split("-")[0] for p in sorted(os.listdir(PRESS_READY_PDF_PATH)) if
                p.lower().endswith('.pdf') and p.lower().startswith('U') ]
    return pdf_list

def save_rows_to_csv(csv_list, writer, status):
    for element in csv_list:
        row = {CSV_HEADERS[0]: element, CSV_HEADERS[1]: status}
        writer.writerow(row)

def update_db(name):
    status = ""
    all_orders = list_of_csv_files()
    orders_in_db = #grab orders from csv_db
    press_ready_pdfs = list_of_press_ready_pdfs()

    current_orders = list(set(all_orders)-set(orders_in_db))

    for o in current_orders:
        if o in press_ready_pdfs:
            status = "done"
        elif o in waiting_pdfs:
            status = "waiting"
        else:
            status = ""

    # loook at current list and make set with the all csv files
    # then for all set check
    with open(csv_file_name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        save_rows_to_csv(csv_list, writer, status)

if __name__ == "__main__":

    name = "csv_missing_db.csv"
    if not os.path.exists(name):
        save_initial_data_to_csv(name)
    else:
        update_db(name)
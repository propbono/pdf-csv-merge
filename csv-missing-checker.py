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
    csv_list = [c.split("-")[0] for c in sorted(os.listdir(SOURCE_CSV_PATH)) if
                c.lower().endswith('.csv')]
    csv_list_toc = timeit.default_timer()
    print("Pdf list - created!", "time (s): ", round(csv_list_toc - csv_list_tic, 4))
    print()

    print("Creating csv db:")
    csv_db_tic = timeit.default_timer()

    with open(name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        save_rows_to_csv(csv_list, writer)


    csv_db_toc = timeit.default_timer()
    print("CSV dict - created!", "time (s): ", round(csv_db_toc - csv_db_tic, 4))


def save_rows_to_csv(csv_list, writer):
    for element in csv_list:
        row = {CSV_HEADERS[0]: element, CSV_HEADERS[1]: "done"}
        writer.writerow(row)

def update_db(name):
      with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            save_rows_to_csv(csv_list, writer)

if __name__ == "__main__":

    name = "csv_missing_db.csv"
    if not os.path.exists(name):
        save_initial_data_to_csv(name)
    else:
        update_db(name)
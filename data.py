import csv
import datetime
import os

from product import Product
from configuration import Configuration
from notes import Notes


class ReturnData(object):
    def __init__(self, processed = 0, skipped = 0, flat = None,
                 bound = None):
        self.files_added_to_csv = processed
        self.files_skipped = skipped
        self.rows_flat = flat or {}
        self.rows_bound = bound or {}


class Data(object):
    def __init__(self, pdf_list = None):
        self.pdf_list = pdf_list
        self.config = Configuration.factory()
        self.CSV_HEADERS_FLAT = ["comment", "Name", "Quantity",
                                         "Width", "Height",
                                         "StockVendor", "StockName",
                                         "StockWeight", "IGNORED1",
                                         "IGNORED2", "Priority", "TopOffcut",
                                         "LeftOffcut",
                                         "BottomOffcut", "RightOffcut",
                                         "ProductID",
                                         "Description", "Notes", "DueDate",
                                         "CompanyName",
                                         "FirstName", "LastName",
                                         "ContentFile", "PageColor1",
                                         "PageColor2", "ProductGroup", "Grain",
                                         "BleedsTop",
                                         "BleedsLeft", "BleedsBottom",
                                         "BleedsRight",
                                         "FolioSide1", "FolioSide2"]

        self.CSV_HEADERS_BOUND_SELF = ["comment", "Name", "Quantity", "Width",
                                       "Height",
                                       "StockVendor", "StockName",
                                       "StockWeight",
                                       "IGNORED0", "TextPageCount",
                                       "LargestTextComponent",
                                       "BindingMachine", "IGNORED1",
                                       "IGNORED2", "IGNORED3",
                                       "ProductID", "Description", "Notes",
                                       "DueDate",
                                       "CompanyName", "FirstName", "LastName",
                                       "ContentFile", "IGNORED4", "INGORED5",
                                       "PageColorName", "IGNORED6",
                                       "BleedsTop",
                                       "BleedsLeft", "BleedsBottom",
                                       "BleedsRight",
                                       "FolioPattern", "TextFolds", "IGNORED7",
                                       "BindingNumberUp", "1stUpOrientation",
                                       "NUpOrientation", "Grain"]


    def __add_data_to_dict(self):
        print("Collecting data to dictionary:")

        data = ReturnData()
        for pdf in self.pdf_list:
            notes = Notes()
            try:
                pdf_without_notes, notes = notes.extract_notes_from(pdf)
            except:
                continue #check impact
            else:
                if notes is None:
                    data.files_skipped += 1
                    print("NOT PREPPED: ", pdf_without_notes[:7])
                else:
                    product = Product.factory(pdf_without_notes, notes)
                    row = product.merge_notes_without_csv()

                    key = notes["stock"]
                    if notes["type"] == "FLAT":
                        data.rows_flat.setdefault(key,[]).append(row)
                    elif notes["type"] == "BOUND":
                        data.rows_bound.setdefault(key, []).append(row)

                    print("ADDED!!: ", pdf[:7])
                    data.files_added_to_csv += 1

        print("All data in dictionary!")
        return data


    def __save_csv_dict_data(self,key, data_dict, headers):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")  # date:
        # 2015-11-03T1935
        dir_name = os.path.join(self.config.MERGED_CSV_LOCAL, today)
        csv_file_name = os.path.join(self.config.MERGED_CSV_LOCAL, dir_name,
                                     key + '-' + now + '.csv')

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        if not os.path.exists(csv_file_name):
            with open(csv_file_name, 'a', newline = '') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = headers)
                writer.writeheader()
                writer.writerows(data_dict)


    def save_all_csv(self):
        dict_data = self.__add_data_to_dict()
        for key in dict_data.rows_flat.keys():
            self.__save_csv_dict_data(key, dict_data.rows_flat[key],
                                  self.CSV_HEADERS_FLAT)
        for key in dict_data.rows_bound.keys():
            self.__save_csv_dict_data(key, dict_data.rows_bound[key],
                                 self.CSV_HEADERS_BOUND_SELF)
        return dict_data


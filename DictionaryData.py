import Product
from Notes import Notes


class Data:
    def __init__(self, processed = 0, skipped = 0, flat = {},
                 bound = {}):
        self.processed_files = processed
        self.skipped_files = skipped
        self.rows_flat = flat
        self.rows_bound = bound

class DictionaryData:
    def __init__(self, pdf_list = None):
        self.pdf_list = pdf_list


    def add_data_to_dict(self):
        data = Data()
        for pdf in self.pdf_list:
            notes = Notes()
            try:
                pdf_without_notes, notes = notes.extract_notes_from(pdf)
            except:
                continue #check impact
            else:
                if notes == None:
                    data.skipped_files += 1
                else:
                    product = Product.Product.factory(pdf_without_notes, notes)
                    row = product.merge_notes_without_csv()

                    key = notes["stock"]
                    if notes["type"] == "FLAT":
                        data.rows_flat.setdefault(key,[]).append(row)
                    elif notes["type"] == "BOUND":
                        data.rows_bound.setdefault(key, []).append(row)

                    print(pdf, " - added!")
                    data.processed_files += 1
        return data


class Product(object):
    @staticmethod
    def factory(pdf, notes):
        type = notes["type"]
        if type == "FLAT": return Flat(pdf, notes)
        if type == "BOUND": return Bound(pdf, notes)
        assert 0, "Bad Product type: " + type

class Flat(Product):
    CSV_HEADERS = ["comment", "Name", "Quantity", "Width", "Height",
                        "StockVendor", "StockName", "StockWeight", "IGNORED1",
                        "IGNORED2", "Priority", "TopOffcut", "LeftOffcut",
                        "BottomOffcut", "RightOffcut", "ProductID",
                        "Description", "Notes", "DueDate", "CompanyName",
                        "FirstName", "LastName", "ContentFile", "PageColor1",
                        "PageColor2", "ProductGroup", "Grain", "BleedsTop",
                        "BleedsLeft", "BleedsBottom", "BleedsRight",
                        "FolioSide1", "FolioSide2"]


    def __init__(self, pdf, notes):
        self.pdf = pdf
        self.notes = notes
        self.row = {"comment": "MetrixCSV2.0_FLAT", "Name": pdf[:-4],
                         "Quantity": notes["quantity"],
                         "Width": notes["width"],
                         "Height": notes["height"], "StockVendor": "PG",
                         "StockName": notes["stockname"],
                         "StockWeight": notes["stockweight"], "IGNORED1": '',
                         "IGNORED2": '', "Priority": '5', "TopOffcut": '0',
                         "LeftOffcut": '0', "BottomOffcut": '0',
                         "RightOffcut": '0',
                         "ProductID": '', "Description": notes["operator"],
                         "Notes": '', "DueDate": '',
                         "CompanyName": pdf.split('-')[2],
                         "FirstName": '', "LastName": '', "ContentFile": '',
                         "PageColor1": '', "PageColor2": '',
                         "ProductGroup": ', "Grain":', "BleedsTop": '0.0625',
                         "BleedsLeft": '0.0625', "BleedsBottom": '0.0625',
                         "BleedsRight": '0.0625',
                         "FolioSide1": "Front", "FolioSide2": "Back"}

    def merge_notes_without_csv(self):
        if "notes" in self.notes:
            self.row["Notes"] = self.notes["notes"]
        self.row["ContentFile"] = self.pdf
        if "group" in self.notes:
            self.row["ProductGroup"] = self.notes["group"]
        if self.notes["stock"] == "d":
            self.row["BleedsBottom"] = "0.125"
            self.row["BleedsRight"] = "0.125"
            self.row["BleedsLeft"] = "0.125"
            self.row["BleedsTop"] = "0.125"
        return self.row

class Bound(Product):
    CSV_HEADERS = ["comment", "Name", "Quantity", "Width", "Height",
                              "StockVendor", "StockName", "StockWeight",
                              "IGNORED0", "TextPageCount",
                              "LargestTextComponent",
                              "BindingMachine", "IGNORED1", "IGNORED2",
                              "IGNORED3",
                              "ProductID", "Description", "Notes", "DueDate",
                              "CompanyName", "FirstName", "LastName",
                              "ContentFile", "IGNORED4", "INGORED5",
                              "PageColorName", "IGNORED6", "BleedsTop",
                              "BleedsLeft", "BleedsBottom", "BleedsRight",
                              "FolioPattern", "TextFolds", "IGNORED7",
                              "BindingNumberUp", "1stUpOrientation",
                              "NUpOrientation", "Grain"]

    def __init__(self, pdf, notes):
        self.pdf = pdf
        self.notes = notes
        self.row = {"comment": "MetrixCSV2.0_BOUND_SELF_COVER", "Name": pdf[:-4],
                    "Quantity": notes["quantity"], "Width": notes["width"],
                    "Height": notes["height"], "StockVendor": "PG",
                    "StockName": notes["stockname"],
                    "StockWeight": notes["stockweight"],
                    "IGNORED0": "", "TextPageCount": "", "LargestTextComponent": "4",
                    "BindingMachine": "DUPLO", "IGNORED1": "", "IGNORED2": "",
                    "IGNORED3": "", "ProductID": "",
                    "Description": notes["operator"], "Notes": "",
                    "DueDate": "", "CompanyName": pdf.split('-')[2],
                    "FirstName": "",
                    "LastName": "", "ContentFile": pdf, "IGNORED4": "",
                    "INGORED5": "",
                    "PageColorName": "Cyan, Magenta, Yellow, Black",
                    "IGNORED6": "",
                    "BleedsTop": "0.0625", "BleedsLeft": "0.0625",
                    "BleedsBottom": "0.0625",
                    "BleedsRight": "0.0625", "FolioPattern": "", "TextFolds": "",
                    "IGNORED7": "", "BindingNumberUp": "",
                    "1stUpOrientation": "HeadToJog",
                    "NUpOrientation": "", "Grain": ""}


    def merge_notes_without_csv(self):
        if "pages" in self.notes:
            self.row["TextPageCount"] = self.notes["pages"]
        if "group" in self.notes:
            self.row["Notes"] = self.notes["group"]
        if "notes" in self.notes:
            self.row["Notes"] += " " + self.notes["notes"]
        if self.notes["stock"] == "d":
            self.row["BleedsBottom"] = "0.125"
            self.row["BleedsRight"] = "0.125"
            self.row["BleedsLeft"] = "0.125"
            self.row["BleedsTop"] = "0.125"

        return self.row
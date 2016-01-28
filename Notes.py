import re

import _operator


class Notes:

    def __init__(self):
        self.notes = {'width': '', 'height': '',
                      "stock": '', 'stockname': '',
                      "stockweight": '', 'quantity': '',
                      'notes': '', 'group': '',
                      'type': '', 'pages': ''}

    def extract_notes_from(self, pdf):
        notes = {}
        try:
            notes_from_pdf = self.__find_prepp_notes(pdf)
        except None:
            self.notes = None
        else:
            if notes_from_pdf:
                notes_from_pdf = notes_from_pdf[0].lstrip('(').rstrip(')').split('-')
                self.notes["width"] = notes_from_pdf[0].split('x')[0]
                self.notes["height"] = notes_from_pdf[0].split('x')[1]
                self.notes["stock"] = notes_from_pdf[1].lower()
                self.notes["quantity"] = pdf.split('-')[-1].rstrip(".pdf")

                for n in notes_from_pdf[2:]:
                    if _operator.contains(n, "n;"):
                        self.notes["notes"] = n.lstrip("n;")
                    elif _operator.contains(n, "g;"):
                        self.notes["group"] = n.lstrip("g;").upper()
                    elif _operator.contains(n, "p;"):
                        self.notes["pages"] = n.lstrip("p;")

            if self.notes['width'] != '':
                self.notes = self.__parse_notes(self.notes)
                pdf = self.__delete_prepp_notes_from(pdf)
        finally:
            return pdf, self.notes

    def __find_prepp_notes(self, pdf):
        text_to_replace = ""
        try:
            text_to_replace = re.findall(r'\(.*\)', pdf)
        except None:
            text_to_replace = None
        finally:
            return text_to_replace

    def __delete_prepp_notes_from(self, pdf):
        try:
            text_to_replace = self.__find_prepp_notes(pdf)
        except None:
            return pdf
        else:
            return pdf.replace(text_to_replace[0], '')

    def __parse_notes(self, notes):
        self.__check_and_correct_stock(notes)
        self.__check_and_crorrect_group(notes)
        self.__add_group_to_notes(notes)
        self.__check_and_crorrect_type(notes)

        if notes["stock"] == "uv" or notes["stock"] == "u":
            notes["group"] = "UV"
        if notes["stock"] == "matte" or notes["stock"] == "m":
            notes["group"] = "MATTE"

        return notes

    def __check_and_correct_stock(self, notes):
        if notes["stock"] == "16pt":
            if int(notes["quantity"]) > 1000:
                notes["stock"] += "5000"
            else:
                notes["stock"] += "1000"

        if _operator.contains(notes["stock"], "16pt"):
            notes["stockname"] = "16pt-Cover"
            notes["stockweight"] = "338"

        if notes["stock"] == "100lb":
            notes["stockname"] = "100lb-Text"
            notes["stockweight"] = "150"

        if notes["stock"] == "80lb":
            notes["stockname"] = "80lb-Text"
            notes["stockweight"] = "115"

        if notes["stock"] == "70lb":
            notes["stockname"] = "70lb-Text"
            notes["stockweight"] = "95"

        if notes["stock"] == "60lb":
            notes["stockname"] = "60lb-Text"
            notes["stockweight"] = "90"

        if notes["stock"] == "18pt":
            notes["stockname"] = "18pt-Matte"
            notes["stockweight"] = "350"

        if notes["stock"] == "10pt":
            notes["stockname"] = "10pt-Cover"
            notes["stockweight"] = "260"

        if notes["stock"] == "12pt":
            notes["stockname"] = "12pt-Cover"
            notes["stockweight"] = "278"

        if notes["stock"] == "14pt":
            notes["stockname"] = "14pt-Cover"
            notes["stockweight"] = "308"

        if notes["stock"] == "8pt":
            notes["stockname"] = "8pt-Cover"
            notes["stockweight"] = "260"

        if notes["stock"] == "70lboffset":
            notes["stockname"] = "70lb-Offset"
            notes["stockweight"] = "95"

        if notes["stock"] == "60lboffset":
            notes["stockname"] = "60lb-Offset"
            notes["stockweight"] = "90"

        if notes["stock"] == "50lboffset":
            notes["stockname"] = "50lb-Offset"
            notes["stockweight"] = "74"

        if notes["pages"] != "":
            notes["stock"] += "magazine"

    def __add_group_to_notes(self, notes):
        notes["notes"] = notes["group"] + " " + notes["notes"]

    def __check_and_crorrect_group(self, notes):
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

    def __check_and_crorrect_type(self, notes):
        if notes["pages"] != "":
            notes["type"] = "BOUND"
        else:
            notes["type"] = "FLAT"
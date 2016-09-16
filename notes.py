import re
import _operator

class Notes(object):

    def __init__(self):
        self.notes = {'width': '', 'height': '',
                      "stock": '', 'stockname': '',
                      "stockweight": '', 'quantity': '',
                      'notes': '', 'group': '',
                      'type': '', 'pages': '', 'is_special':''}
        self.SPECIAL_NOTES = "stamp,drill,notepad,notepads,special,track," \
                             "scoring".upper().split(",")
        self.SPECIAL_GROUPS = "d,diecut,s,sameday,u,urgent,r," \
                         "roundcorner,p,presssample,n,noaq,f," \
                         "foilstamp,e,emboss,sc,score,fedex,x".upper().split(
                ",")


        self.GROUPS = {"D": "DIECUT", "O": "ONESIDED", "S": "SAMEDAY", "U": "URGENT",
               "R": "ROUNDCORNER", "P": "PRESSSAMPLE", "M": "MATTE",
               "N": "NOAQ",
               "F": "FOILSTAMP", "E": "EMBOSS", "SC": "SCORE", "X":"FEDEX"}

    def extract_notes(self, pdf):
        try:
            notes_from_pdf = self._find_prepp_notes(pdf)
        except Exception as e:
            print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        else:
            if notes_from_pdf:
                name = pdf.split('-')[2].lower()
                notes_from_pdf = notes_from_pdf[0].lstrip('(').rstrip(')').split('-')
                self.notes["width"] = notes_from_pdf[0].lower().split('x')[0]
                self.notes["height"] = notes_from_pdf[0].lower().split('x')[1]
                self.notes["stock"] = notes_from_pdf[1].lower()
                self.notes["quantity"] = pdf.split('-')[-1].rstrip(".pdf")

                for note in notes_from_pdf[2:]:
                    if _operator.contains(note, "n;"):
                        self.notes["notes"] = note.lstrip("n;")
                    elif _operator.contains(note, "g;"):
                        self.notes["group"] =  note.lstrip("g;").upper()
                    elif _operator.contains(note, "p;"):
                        self.notes["pages"] = note.lstrip("p;")
                    elif note.lower() == 't' or note.lower() == 't;':
                        self.notes["is_special"] = "special"
                if _operator.contains(name, "fedex"):
                    if self.notes["group"] == "":
                        self.notes["group"] = "x".upper()
                    else:
                        self.notes["group"] +=",x".upper()

                self.notes = self._parse_notes(self.notes)
                pdf = self.delete_prepp_notes_from(pdf)
            else:
                self.notes = None
        finally:
            return pdf, self.notes

    def delete_prepp_notes_from(self, pdf):
        try:
            text_to_replace = self._find_prepp_notes(pdf)
        except Exception as e:
            print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        else:
            if text_to_replace is None:
                return  pdf
            else:
                return pdf.replace(text_to_replace[0], '')

    def _find_prepp_notes(self, pdf):
        text_to_replace = None
        try:
            text_to_replace = re.findall(r'\(.*\)', pdf)
        except Exception as e:
            print("Error '{0}' occured. Arguments {1}.".format(e, e.args))
        finally:
            if text_to_replace == []:
                return None
            else:
                return text_to_replace

    def _parse_notes(self, notes):
        notes = self._check_and_correct_stock(notes)
        notes = self._check_and_crorrect_group(notes)
        notes = self._add_group_to_notes(notes)
        notes = self._check_and_crorrect_type(notes)

        notes = self._correct_uv_matte_stock(notes)

        notes = self._check_if_special(notes)

        return notes

    def _correct_uv_matte_stock(self, notes):
        if notes["stock"] == "uv" or notes["stock"] == "u":
            notes["group"] = "UV"
            self._add_group_to_notes(notes)
        if notes["stock"] == "matte" or notes["stock"] == "m":
            notes["group"] = "MATTE"
            self._add_group_to_notes(notes)
        return notes

    def _check_and_correct_stock(self, notes):

        if notes["stock"] == "16pt":
            if int(notes["quantity"]) > 1000:
                notes["stock"] += "5000"
            else:
                notes["stock"] += "1000"

        if _operator.contains(notes["stock"], "16pt") or notes["stock"] == \
                "uv" or notes["stock"] == "matte":
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

        if notes["stock"] == "8pt":
            notes["stockname"] = "8pt-Cover"
            notes["stockweight"] = "260"

        if notes["stock"] == "10pt":
            notes["stockname"] = "10pt-Cover"
            notes["stockweight"] = "260"

        if notes["stock"] == "12pt":
            notes["stockname"] = "12pt-Cover"
            notes["stockweight"] = "278"

        if notes["stock"] == "14pt":
            notes["stockname"] = "14pt-Cover"
            notes["stockweight"] = "308"

        if notes["stock"] == "13pt":
            notes["stockname"] = "13pt-Enviro"
            notes["stockweight"] = "290"

        if notes["stock"] == "24pt":
            notes["stockname"] = "24pt-Cover"
            notes["stockweight"] = "350"

        if notes["stock"] == "15pt":
            notes["stockname"] = "15pt-C1S"
            notes["stockweight"] = "308"

        if notes["stock"] == "70lboffset":
            notes["stockname"] = "70lb-Offset"
            notes["stockweight"] = "95"

        if notes["stock"] == "60lboffset":
            notes["stockname"] = "60lb-Offset"
            notes["stockweight"] = "90"

        if notes["stock"] == "50lboffset":
            notes["stockname"] = "50lb-Offset"
            notes["stockweight"] = "74"

        if notes["stock"] =="qm":
            notes["stockname"] = "QM"
            notes["stockweight"] = "20"

        if notes["stock"] == "digital" or notes["stock"] == "d":
            notes["stockname"] = "Digital"
            notes["stockweight"] = "150"

        if notes["pages"] != "":
            notes["stock"] += "magazine"
            notes["notes"] += " BOOKLET"
        return notes

    def _add_group_to_notes(self, notes):
        notes["notes"] = notes["group"] + " " + notes["notes"]
        return notes

    def _check_and_crorrect_group(self, notes):
        if notes["group"] == "D":
            notes["group"] = "DIECUT"
        elif notes["group"] == "O":
            notes["group"] = "ONESIDED"
        elif notes["group"] == "S":
            notes["group"] = "SAMEDAY"
        elif notes["group"] == "U":
            notes["group"] = "URGENT"
        elif notes["group"] == "R":
            notes["group"] = "ROUNDCORNER"
        elif notes["group"] == "P":
            notes["group"] = "PRESSSAMPLE"
        elif notes["group"] == "M":
            notes["group"] = "MATTE"
        elif notes["group"] == "N":
            notes["group"] = "NOAQ"

        elif notes["group"] == "F":
            notes["group"] = "FOILSTAMP"
        elif notes["group"] == "E":
            notes["group"] = "EMBOSS"
        elif notes["group"] == "SC":
            notes["group"] = "SCORE"
        elif notes["group"] == "X":
            notes["group"] = "FEDEX"
        elif self._check_if_mixed_group(notes["group"]):
            notes["notes"] += self._correct_notes_for_mixed_group(notes["group"])
            notes["group"] = "MIXED"
        elif _operator.contains(notes["group"], ","):
            notes["group"] = ""
        return notes

    def _check_and_crorrect_type(self, notes):
        if notes["pages"] != "":
            notes["type"] = "BOUND"
        else:
            notes["type"] = "FLAT"

        return notes

    def _check_if_special(self, notes):
        if notes["is_special"] is "":
            if self._check_if_special_group(notes) or \
                    self._check_if_special_note(notes):
                notes["is_special"] = "special"
        return notes

    def _check_if_special_group(self, notes):
        for group in notes["group"].split(","):
            if group in self.SPECIAL_GROUPS:
                return True

    def _check_if_mixed_group(self, notes):
        group_to_check = notes.split(",")
        is_mixed = [i for i in group_to_check if i in self.GROUPS.keys()]
        return is_mixed

    def _check_if_special_note(self, notes):
        notes_to_check = notes["notes"].upper().split(" ")
        return [i for i in notes_to_check if i in self.SPECIAL_NOTES]

    def _correct_notes_for_mixed_group(self, notes):
        groups = ""
        for n in notes.split(','):
            groups += " " + self.GROUPS[n]
        return groups

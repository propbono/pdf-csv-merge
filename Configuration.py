import os
import sys
#
class Configuration(object):
    init_type = "Debug"
    @staticmethod
    def factory(type=init_type):
        if type == "Debug": return Debug()
        if type == "Working": return Working()
        assert 0, "Bad configuration type: " + type


class Debug(Configuration):
    # First check what pdf files we have in the folder
    DIR = os.path.dirname(sys.argv[0])

    PREPPED_PDF_PATH = os.path.join(DIR, "pdf")
    PRESS_READY_PDF_PATH = os.path.join(DIR, "pdf")
    SOURCE_CSV_PATH = "O:\\"
    MERGED_CSV_REMOTE = os.path.join(DIR, "merged_csv_remote")
    PREPPED_PDF_DONE_PATH = os.path.join(PREPPED_PDF_PATH, "00Done")
    MERGED_CSV_LOCAL = os.path.join(DIR, "merged_csv")

class Working(Configuration):
    # First check what pdf files we have in the folder
    DIR = os.path.dirname(sys.argv[0])

    PREPPED_PDF_PATH = "N:\\"
    PRESS_READY_PDF_PATH = "Q:\\"
    SOURCE_CSV_PATH = "O:\\"
    MERGED_CSV_REMOTE = "K:\\"
    PREPPED_PDF_DONE_PATH = os.path.join(PREPPED_PDF_PATH, "00Done")
    MERGED_CSV_LOCAL = os.path.join(DIR, "merged_csv")
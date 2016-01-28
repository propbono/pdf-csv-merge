import datetime
import os
import shutil

from Configuration import Configuration

from Notes import Notes


class Move:
    def __init__(self):
        self.config = Configuration.type

    @staticmethod
    def rename_and_move_pdf(pdf_list):
        for i, pdf in enumerate(pdf_list, 1):
            new_pdf = Notes.delete_prepp_notes_from(pdf)
            self.__copy_pdf_to_done_folder(pdf)
            self.__move_pdf_to_press_ready_pdf(pdf, new_pdf)
            print(i, " *" * i)

    @staticmethod
    def move_merged_csv():
        today = datetime.date.today().isoformat()
        remote_dir_name = os.path.join(self.config.MERGED_CSV_REMOTE, today)
        if not os.path.isdir(remote_dir_name):
            os.mkdir(remote_dir_name)

        local_csv_list = os.listdir(
                os.path.join(self.config.MERGED_CSV_LOCAL, today))
        for csv_name in local_csv_list:
            shutil.copy(
                os.path.join(self.config.MERGED_CSV_LOCAL, today, csv_name),
                os.path.join(self.config.MERGED_CSV_REMOTE, today, csv_name))

    def __move_pdf_to_press_ready_pdf(self, name, new_name):
        shutil.move(os.path.join(self.config.PREPPED_PDF_PATH, name),
                    os.path.join(self.config.PRESS_READY_PDF_PATH, new_name))

    def __copy_pdf_to_done_folder(self, pdf):
        shutil.copyfile(os.path.join(
                self.config.PREPPED_PDF_PATH, pdf),
                os.path.join(
                        self.config.PREPPED_PDF_DONE_PATH, pdf))

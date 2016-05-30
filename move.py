import datetime
import os
import shutil
import timeit

from configuration import Configuration

from Notes import Notes


class Move(object):
    def __init__(self):
        self.config = Configuration.factory()
        self.pdf_to_delete = []


    def rename_and_move_pdf(self, pdf_list):
        press_ready_pdf_list = self.__press_ready_pdf_list()
        for i, pdf in enumerate(pdf_list, 1):
            tic = timeit.default_timer()
            notes = Notes()
            new_pdf = notes.delete_prepp_notes_from(pdf)
            if new_pdf in press_ready_pdf_list:
                self.pdf_to_delete.append(pdf)
                toc = timeit.default_timer()
                print(i, new_pdf[:7], "NOT MOVED, time: ", round(toc - tic, 4), "s")
            else:
                self.__copy_pdf_to_done_folder(pdf)
                self.__move_pdf_to_press_ready_pdf(pdf, new_pdf)
                toc = timeit.default_timer()
                print(i, new_pdf[:7], "MOVED, time: ", round(toc - tic, 4), "s")
        return self.pdf_to_delete

    def __press_ready_pdf_list(self):
        press_ready_pdf_list = [p for p in sorted(
            os.listdir(self.config.PRESS_READY_PDF_PATH)) if p.upper().startswith("U") and p.lower().endswith('.pdf')]
        return press_ready_pdf_list

    def move_merged_csv(self):
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
        shutil.copyfile(os.path.join(self.config.PREPPED_PDF_PATH, pdf),
                os.path.join(self.config.PREPPED_PDF_DONE_PATH, pdf))

    def delete_unused_pdf(self, pdf_list):
        for pdf in pdf_list:
            os.remove(os.path.join(self.config.PREPPED_PDF_PATH, pdf))
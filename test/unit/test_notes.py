import unittest

import notes
from notes import Notes


class TestNotes(unittest.TestCase):

    def make_arrangements(self, name = None):
        notes = Notes()
        pdf_name = name or "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-18pt-g;urgent)-500.pdf"
        pdf, parsed_notes = notes.extract_notes(pdf_name)
        return pdf, parsed_notes

    def test_extract_notes_when_group_is_provided_group_is_not_empty(self):
        pdf, parsed_notes = self.make_arrangements()
        self.assertIsNot("", parsed_notes["group"],msg = "Group is empty")

    def test_extract_notes_when_group_small_caps_group_returns_allcaps_group(self):
        pdf, parsed_notes = self.make_arrangements()
        self.assertEqual(parsed_notes["group"], parsed_notes["group"].upper(), msg = "Group Should br all caps")

    def test__check_if_special_returns_special_when_sameday(self):
        notes = Notes()
        notes_to_check =  {'width': '', 'height': '', 'stock': '',
                           'stockname': '', 'stockweight': '', 'quantity': '', 'notes': '',
                           'group': 'S', 'type': '', 'pages': '', 'is_special': ''}

        result_notes = notes._check_if_special(notes_to_check)

        self.assertEqual("special", result_notes["is_special"], "Groups are "
                                                                "different")

    def test__check_if_special_returns_special_when_emboss(self):
        notes = Notes()
        notes_to_check = {'width': '', 'height': '', 'stock': '',
                          'stockname': '', 'stockweight': '', 'quantity': '',
                          'notes': '',
                          'group': 'EMBOSS', 'type': '', 'pages': '',
                          'is_special': ''}

        result_notes = notes._check_if_special(notes_to_check)

        self.assertEqual("special", result_notes["is_special"], "Groups are "
                                                                "different")

    def test__check_if_special_returns_special_when_special_notes_drill(self):
        notes = Notes()
        notes_to_check = {'width': '', 'height': '', 'stock': '',
                          'stockname': '', 'stockweight': '', 'quantity': '',
                          'notes': 'drill scoring tracK ',
                          'group': '', 'type': '', 'pages': '',
                          'is_special': ''}

        result_notes = notes._check_if_special(notes_to_check)

        self.assertEqual("special", result_notes["is_special"], "There is no special note in notes['notes']")

    def test_extract_notes_when_group_sameday_is_special_set_to_special(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-18pt-g;s)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual( "special", parsed_notes["is_special"], msg = "ups note should be special")

    def test_extract_notes_when_special_note_is_special_set_to_special(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-18pt-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("special", parsed_notes["is_special"], msg = "ups note should be special")

    def test_extract_notes_when_stock_uv_group_should_be_UV(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-uv-g;o-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual(parsed_notes["group"], "UV", msg = "group should be UV")

    def test_extract_notes_when_stock_uv_notes_should_be_UV(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-uv-g;o-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        splited_notes = parsed_notes["notes"].split(" ")

        self.assertIn("UV", splited_notes, "Notes should have UV")

    def test_extract_notes_when_stock_uv_with_group_o_notes_should_be_UV_ONESIDED(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-uv-g;o-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        splited_notes = parsed_notes["notes"].split(" ")

        self.assertIn("UV", splited_notes, "Notes should have UV in it")
        self.assertIn("ONESIDED", splited_notes, "Notes should have ONESIDED in it")

    def test_extract_notes_when_group_sd_group_should_be_MIXED(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-16pt-g;s,d-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("MIXED", parsed_notes["group"], msg = "group should be MIXED")

    def test_extract_notes_when_UV_and_group_sd_group_should_be_UV(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-uv-g;s,d-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("UV", parsed_notes["group"], msg = "group should be UV")

    def test_extract_notes_when_group_sdm_group_should_be_MIXED(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-16pt-g;s,d,m-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual( "MIXED", parsed_notes["group"], msg = "group should be MIXED")

    def test_extract_notes_when_group_sdmsc_group_should_be_MIXED(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-16pt-g;s,d,m,sc-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("MIXED", parsed_notes["group"], msg = "group should be MIXED")

    def test_extract_notes_when_group_comma_group_should_be_empty(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-16pt-g;,-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("", parsed_notes["group"], msg = "There should not be any group")

    def test_extract_notes_when_group_sdm_notes_should_be_SAMEDAY_DIECUT_MATTE(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-16pt-g;s,d,m-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        splited_notes = parsed_notes["notes"].split(" ")

        self.assertIn("SAMEDAY", splited_notes, "Notes should have SAMEDAY in it")
        self.assertIn("DIECUT", splited_notes, "Notes should have DIECUT in it")
        self.assertIn("MATTE", splited_notes, "Notes should have MATTE in it")

    def test_extract_notes_when_UV_and_group_sdm_notes_should_be_UV_SAMEDAY_DIECUT_MATTE(self):
        pdf_name = "U100030-S100030-BossImageInc-LixarAsafKarpel(3.5x2-uv-g;s,d-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        splited_notes = parsed_notes["notes"].split(" ")

        self.assertIn("SAMEDAY", splited_notes, "Notes should have SAMEDAY in it")
        self.assertIn("DIECUT", splited_notes, "Notes should have DIECUT in it")
        self.assertIn("UV", splited_notes, "Notes should have UV in it")

    def test_extract_notes_when_company_name_fedex_and_no_group_group_should_be_x(self):
        pdf_name = "U100030-S100030-Fedex-LixarAsafKarpel(3.5x2-16pt-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("FEDEX", parsed_notes["group"], msg = "The group should be FEDEX")

    def test_extract_notes_when_company_name_fedex_and_group_s_group_should_be_sx(self):
        pdf_name = "U100030-S100030-Fedex-LixarAsafKarpel(3.5x2-16pt-g;s-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        self.assertEqual("MIXED", parsed_notes["group"], msg = "The group should be MIXED")

    def test_extract_notes_when_company_name_fedex_and_group_sdm_notes_should_be_FEDEX_SAMEDAY_DIECUT_MATTE(self):
        pdf_name = "U100030-S100030-fedex-LixarAsafKarpel(3.5x2-uv-g;s,d-n;drill)-500.pdf"
        pdf, parsed_notes = self.make_arrangements(pdf_name)
        splited_notes = parsed_notes["notes"].split(" ")

        self.assertIn("SAMEDAY", splited_notes, "Notes should have SAMEDAY in it")
        self.assertIn("DIECUT", splited_notes, "Notes should have DIECUT in it")
        self.assertIn("UV", splited_notes, "Notes should have UV in it")
        self.assertIn("FEDEX", splited_notes, "Notes should have FEDEX in it")

if __name__ == "__main__":
    unittest.main()

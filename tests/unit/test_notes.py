import unittest
from unittest import TestCase

from notes import Notes


class TestNotes(TestCase):


    def setUp(self):
        self.parser = Notes()
        self.name = "U144499-S144499-MayakCanadaInc-NutriLawnCircleAisling(2.5x2.5-16pt-g;d-n;7 names the same upload number different quantities)-100.pdf"


    def test_extract_notes_from_returns_pdf_name_without_notes(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertEqual("U144499-S144499-MayakCanadaInc-NutriLawnCircleAisling-100.pdf",pdf, "Pdf name is incorrect notes was not deleted")

    def test_extract_notes_from_returns_width(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertEqual("2.5", notes['width'], "Width is not correct")

    def test_extract_notes_from_returns_height(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertEqual("2.5", notes['height'], "Height is not correct")

    def test_extract_notes_from_returns_stock(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertNotEqual("", notes['stock'], "Stock information is missing")

    def test_extract_notes_from_returns_stock_as_small_caps(self):
        name = "U144499-S144499-MayakCanadaInc-NutriLawnCircleAisling(2.5x2.5-60lbOffset-g;d-n;7 names the same upload number different quantities)-100"
        pdf, notes = self.parser.extract_notes_from(name)
        self.assertEqual("60lboffset", notes['stock'], "Stock information is not in small caps")

    def test_extract_notes_from_returns_16pt1000_for_quantity_less_equall_1000(self):
        name = "U144499-S144499-MayakCanadaInc-NutriLawnCircleAisling(2.5x2.5-16pt-g;d-n;7 names the same upload number different quantities)-100"
        pdf, notes = self.parser.extract_notes_from(name)
        self.assertEqual("16pt1000", notes['stock'], "Stock information is not in small caps")

    def test_extract_notes_from_returns_16pt5000_for_quantity_less_equall_1000(self):
        name = "U144499-S144499-MayakCanadaInc-NutriLawnCircleAisling(2.5x2.5-16pt-g;d-n;7 names the same upload number different quantities)-1500"
        pdf, notes = self.parser.extract_notes_from(name)
        self.assertEqual("16pt5000", notes['stock'], "Stock information is not in small caps")

    def test_extract_notes_from_returns_notes(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertNotEqual("", notes['notes'], "Notes information is missing")

    def test_extract_notes_from_returns_group(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertNotEqual("", notes['notes'], "Stock information is missing")

    def test_extract_notes_from_returns_proper_quantity(self):
        pdf, notes = self.parser.extract_notes_from(self.name)
        self.assertEqual("100", notes['quantity'], "Quantity is not correct")




    def test_delete_prepp_notes_from(self):
        self.fail()


if __name__ == "__main__":
    unittest.main()
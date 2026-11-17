from main import extract_title
import unittest


class Test_Main(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(extract_title("# Hello my bro"), "Hello my bro")

    def test_extract_title_spaces(self):
        self.assertEqual(extract_title("# Hello  my_bro"), "Hello  my_bro")

    def test_extract_title_almost_h1(self):
        self.assertRaises(
            Exception, extract_title, "#  I am not a title ('cause i have two spaces)"
        )

    def test_extract_title_symbols(self):
        self.assertEqual(
            extract_title(
                "# Yoh, M4_Br073r & `Fr13nd$$` ('Hacker' or rapper heheh) - **An amazing adventure** [_part one_]"
            ),
            "Yoh, M4_Br073r & `Fr13nd$$` ('Hacker' or rapper heheh) - **An amazing adventure** [_part one_]",
        )


if __name__ == "__main__":
    unittest.main()

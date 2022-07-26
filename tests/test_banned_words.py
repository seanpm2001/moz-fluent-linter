import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestBannedWords(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "file.ftl", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testCO01(self):
        content = """
excluded-word = Set up your alias

# Comment should be ignored when displaying the offset of the error
excluded-word2 = Set up Your Alias
excluded-word3 = Set up Your <b>alias</b>
excluded-word4 = <b>Set up Your Alias Now</b>
bad-ignored = Alias

excluded_sentence1 = This is a black list
excluded_sentence2 = This is a <b>black list</b>

"""

        config = {
            "CO02": {
                "enabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        config = {
            "CO02": {
                "enabled": True,
                "words": ["alias", "Black List"],
                "exclusions": {
                    "messages": ["bad-ignored"],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 6)
        self.assertTrue("CO02" in results[0])
        self.assertTrue("line 5" in results[1])
        self.assertTrue("alias" in results[0])
        self.assertTrue("black list" in results[5])

        config = {
            "CO01": {
                "enabled": True,
                "words": ["alias", "black list"],
                "exclusions": {
                    "files": ["file.ftl"],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

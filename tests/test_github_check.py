import unittest
from pylint_github_issue_links import github_check


class TestFunctions(unittest.TestCase):
    def test_get_links_from_line(self) -> None:
        test_cases = [
            ("https://api.github.com/repos/microsoft/pyright/issues/4465", ["https://api.github.com/repos/microsoft/pyright/issues/4465"]),
            ("api.github.com/repos/microsoft/pyright/issues/4465", ["api.github.com/repos/microsoft/pyright/issues/4465"]),
            ("https://github.com/microsoft/pyright/issues/4465", ["https://github.com/microsoft/pyright/issues/4465"]),
            ("https://www.github.com/microsoft/pyright/issues/4465", ["https://www.github.com/microsoft/pyright/issues/4465"]),
            ("github.com/microsoft/pyright/issues/4465", ["github.com/microsoft/pyright/issues/4465"]),
            ("www.github.com/microsoft/pyright/issues/4465", ["www.github.com/microsoft/pyright/issues/4465"]),
            ("www.github.com/microsoft/pyright", []),
            ("asdf", []),
            ("balisehgiha sleighalsdk fjlaksdjf", []),
            ("asdfgithub.com/microsoft/pyright/issues/4465 asd ighelaihdlijga", ["github.com/microsoft/pyright/issues/4465"]),
            ("github.com/microsoft/pyright/issues/4465 and github.com/microsoft/pyright/issues/4465",["github.com/microsoft/pyright/issues/4465","github.com/microsoft/pyright/issues/4465"]),
        ]

        for line, expected_results in test_cases:
            with self.subTest(line=line):
                self.assertListEqual(github_check.get_links_from_line(line), expected_results)
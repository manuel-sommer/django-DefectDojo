from .dojo_test_case import DojoTestCase, get_unit_tests_path
import os
import re

basedir = os.path.join(get_unit_tests_path(), '..')


class TestParsers(DojoTestCase):
    def test_file_existence(self):
        for parser_dir in os.scandir(os.path.join(basedir, 'dojo', 'tools')):

            if parser_dir.is_file() or parser_dir.name == '__pycache__':
                continue  # this is not parser dir but some support file

            if parser_dir.name.startswith("api_"):
                doc_name = parser_dir.name[4:]
                category = 'api'
            else:
                doc_name = parser_dir.name
                category = 'file'

            if doc_name not in [
                'checkmarx_osa',  # it is documented in 'checkmarx'
            ]:
                with self.subTest(parser=parser_dir.name, category='docs'):
                    doc_file = os.path.join(basedir, 'docs', 'content', 'en', 'integrations', 'parsers', category, f"{doc_name}.md")
                    self.assertTrue(
                        os.path.isfile(doc_file),
                        f"Documentation file '{doc_file}' is missing or using different name"
                    )

            if parser_dir.name not in [
                # there is not exception for now
            ]:
                with self.subTest(parser=parser_dir.name, category='parser'):
                    parser_test_file = os.path.join(basedir, 'unittests', 'tools', f"test_{parser_dir.name}_parser.py")
                    self.assertTrue(
                        os.path.isfile(parser_test_file),
                        f"Unittest of parser '{parser_test_file}' is missing or using different name"
                    )

            if parser_dir.name not in [
                'vcg',  # content of the sample report is string the directly in unittest
            ]:
                with self.subTest(parser=parser_dir.name, category='testfiles'):
                    scan_dir = os.path.join(basedir, 'unittests', 'scans', parser_dir.name)
                    self.assertTrue(
                        os.path.isdir(scan_dir),
                        f"Test files for unittest of parser '{scan_dir}' are missing or using different name"
                    )

            if category == 'api':
                if parser_dir.name not in [
                    'api_blackduck',  # TODO
                    'api_vulners',  # TODO
                ]:
                    with self.subTest(parser=parser_dir.name, category='importer'):
                        importer_test_file = os.path.join(basedir, 'unittests', 'tools', f"test_{parser_dir.name}_importer.py")
                        self.assertTrue(
                            os.path.isfile(importer_test_file),
                            f"Unittest of importer '{importer_test_file}' is missing or using different name"
                        )

            for file in os.scandir(os.path.join(basedir, 'dojo', 'tools', parser_dir.name)):
                if file.is_file() and file.name not in ['__pycache__', "__init__.py"]:
                    f = os.path.join(basedir, 'dojo', 'tools', parser_dir.name, file.name)
                    read_true = False
                    with self.subTest(parser=parser_dir.name, category='read()'):
                        with open(f) as fp:
                            for line in fp:
                                if read_true:
                                    if (re.search(r"[\"']utf-8(-sig)?[\"']", line)) and i <= 4:
                                        read_true = False
                                        i = 0
                                    elif i > 4:
                                        self.assertTrue(False, f"In file {f}, the test is failing because you don't have utf-8 after .read()")
                                        i = 0
                                        read_true = False
                                    else:
                                        i += 1
                                if ".read()" in line:
                                    read_true = True
                                    i = 0

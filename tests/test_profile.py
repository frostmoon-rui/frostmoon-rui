import sys
import re
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from update_profile import collect, render


class ProfileTests(unittest.TestCase):
    def test_counts_only_public_owned_repository_stars(self):
        def get(path):
            if '/repos?' not in path:
                return {'followers': 2}
            return [{'stargazers_count': 3, 'forks_count': 4},
                    {'fork': True, 'stargazers_count': 999}, {'private': True, 'stargazers_count': 999}]
        self.assertEqual(dict(collect(get)), {'PUBLIC REPOS': 2, 'STARS EARNED': 3, 'FOLLOWERS': 2, 'FORKS RECEIVED': 4})

    def test_generated_svg_escapes_labels(self):
        root = ET.fromstring(render([('A & B < C', 0)], '2026-10-18'))
        self.assertEqual(root.attrib['role'], 'img')
        self.assertIn('A & B < C', ''.join(root.itertext()))

    def test_local_artwork_is_valid_svg(self):
        root = Path(__file__).resolve().parents[1]
        for name in ('banner.svg', 'toolbox.svg', 'activity.svg'):
            with self.subTest(name=name):
                image = ET.parse(root / 'assets' / name).getroot()
                self.assertTrue(image.tag.endswith('svg'))
                self.assertEqual(image.attrib['role'], 'img')

    def test_public_profile_technical_content(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')
        for technology in ('C / C++', 'MATLAB', 'Python', 'LaTeX', 'Simpson', 'VBA'):
            self.assertIn(technology, readme)
        for private_field in ('legal name', 'contact details', 'education history',
                              'birth date', 'resume', '\u59d3\u540d', '\u8054\u7cfb\u65b9\u5f0f',
                              '\u6559\u80b2\u80cc\u666f', '\u6bd5\u4e1a\u9662\u6821',
                              '\u51fa\u751f\u65e5\u671f', '\u4e2a\u4eba\u7b80\u5386'):
            self.assertNotIn(private_field, readme)

    def test_tracked_text_contains_no_han_characters(self):
        root = Path(__file__).resolve().parents[1]
        git = shutil.which('git')
        if git is None and sys.platform == 'win32':
            git = 'C:/Program Files/Git/cmd/git.exe'
        self.assertIsNotNone(git, 'Git is required to enumerate tracked profile files')
        tracked = subprocess.check_output(
            [git, '-c', f'safe.directory={root.as_posix()}', 'ls-files', '-z'], cwd=root
        ).decode('utf-8').split('\0')
        han = re.compile('[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'
                         '\U00020000-\U0002ffff\U00030000-\U0003347f]')
        for name in filter(None, tracked):
            with self.subTest(name=name):
                data = (root / name).read_bytes()
                if b'\0' in data:
                    continue
                try:
                    content = data.decode('utf-8-sig')
                except UnicodeDecodeError:
                    continue
                self.assertIsNone(han.search(content), f'Han characters found in {name}')


if __name__ == '__main__':
    unittest.main()

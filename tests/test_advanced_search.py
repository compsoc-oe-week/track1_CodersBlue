import unittest
import os
import shutil
import sys
from datetime import datetime, timedelta

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.search import find_files

class TestAdvancedSearch(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_advanced_search_dir'
        os.makedirs(self.test_dir, exist_ok=True)

        # Create files with different sizes and modification times
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('a' * 10) # 10 bytes

        with open(os.path.join(self.test_dir, 'file2.log'), 'w') as f:
            f.write('b' * 1024) # 1 KB

        with open(os.path.join(self.test_dir, 'file3.pdf'), 'w') as f:
            f.write('c' * 2048) # 2 KB

        # Set modification times
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        os.utime(os.path.join(self.test_dir, 'file1.txt'), (yesterday.timestamp(), yesterday.timestamp()))
        os.utime(os.path.join(self.test_dir, 'file2.log'), (last_week.timestamp(), last_week.timestamp()))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_size_filtering(self):
        # Test for files larger than 500 bytes
        found_files = find_files('*', path=self.test_dir, size='>500B')
        self.assertEqual(len(found_files), 2)

        # Test for files smaller than 1.5 KB (1536 bytes)
        # Using bytes to avoid float parsing issues for now
        found_files = find_files('*', path=self.test_dir, size='<1536B')
        self.assertEqual(len(found_files), 2)

    def test_date_filtering(self):
        # Test for files modified in the last 2 days
        found_files = find_files('*', path=self.test_dir, modified='<2d')
        # Expecting file1.txt (yesterday) and file3.pdf (now)
        self.assertEqual(len(found_files), 2)

        # Test for files modified more than 3 days ago
        found_files = find_files('*', path=self.test_dir, modified='>3d')
        self.assertEqual(len(found_files), 1)

    def test_type_filtering(self):
        # Test for documents
        found_files = find_files('*', path=self.test_dir, file_type='documents')
        # Expecting file1.txt and file3.pdf
        self.assertEqual(len(found_files), 2)

        # Test for logs
        found_files = find_files('*', path=self.test_dir, file_type='logs')
        self.assertEqual(len(found_files), 1)

if __name__ == '__main__':
    unittest.main()
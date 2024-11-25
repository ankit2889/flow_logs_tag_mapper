import unittest
import os
import sys

# Add the scripts directory to the module search path for imports during testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from flow_logs_parser import generate_counts

class TestGenerateCounts(unittest.TestCase):

    def setUp(self):
        self.flow_log_file = os.path.join(os.getcwd(),'tests/resources/flow_logs.txt')
        self.tags_file = os.path.join(os.getcwd(),'tests/resources/tags.csv')

    def test_generate_counts(self):
        """Test the generate_counts function with the 'tag' and 'dstport_protocol' keyword"""

        # Expected result for 'tag' keyword
        expected_tag_counts = {
            'untagged': 8, 
            'email': 3, 
            'sv_P1': 2, 
            'sv_P2': 1
        }

        # Run the method and compare the result
        tag_counter, port_protocol_counter = generate_counts(self.flow_log_file, self.tags_file)
        self.assertEqual(tag_counter, expected_tag_counts)

         # Expected result for 'dstport_protocol' keyword
        expected_port_protocol_counts = {
            '49153,tcp': 1,
            '49154,tcp': 1,
            '49155,tcp': 1,
            '49156,tcp': 1,
            '49157,tcp': 1,
            '49158,tcp': 1,
            '80,tcp': 1,
            '1024,tcp': 1,
            '443,tcp': 1,
            '23,tcp': 1,
            '25,tcp': 1,
            '110,tcp': 1,
            '993,tcp': 1,
            '143,tcp': 1
        }
    
        self.assertEqual(port_protocol_counter, expected_port_protocol_counts)

    def test_generate_counts_invalid(self):
        """Test case when no flow logs or tags are returned"""
        
        with self.assertRaises(Exception):
            generate_counts('invalid_path', 'invalid_tags_path', keyword='tag')

if __name__ == '__main__':
    unittest.main()
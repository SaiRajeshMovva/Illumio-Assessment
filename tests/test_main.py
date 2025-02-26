import unittest
import tempfile
import os
from io import StringIO
import sys

from main import load_lookup, parse_flow_logs, output_results, PROTOCOL_MAP


class TestFlowTag(unittest.TestCase):
    def setUp(self):
        # Create temporary files for lookup CSV and flow log data
        self.lookup_content = (
            "dstport,protocol,tag\n"
            "443,tcp,sv_P2\n"
            "23,tcp,sv_P1\n"
            "80,tcp,sv_P3\n"
        )
        self.flow_log_content = (
            "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 1234 443 6 25 20000 1620140761 1620140821 ACCEPT OK\n"
            "2 123456789012 eni-0a1b2c3d 10.0.1.202 198.51.100.3 1234 1024 6 25 20000 1620140761 1620140821 ACCEPT OK\n"
            "2 123456789012 eni-0a1b2c3d 10.0.1.203 198.51.100.4 1234 23 6 25 20000 1620140761 1620140821 ACCEPT OK\n"
        )
        # Create temporary lookup file
        self.temp_lookup = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii')
        self.temp_lookup.write(self.lookup_content)
        self.temp_lookup.close()
        
        # Create temporary flow log file
        self.temp_flow = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii')
        self.temp_flow.write(self.flow_log_content)
        self.temp_flow.close()

    def tearDown(self):
        os.unlink(self.temp_lookup.name)
        os.unlink(self.temp_flow.name)

    def test_load_lookup(self):
        lookup = load_lookup(self.temp_lookup.name)
        expected_lookup = {
            ("443", "tcp"): "sv_P2",
            ("23", "tcp"): "sv_P1",
            ("80", "tcp"): "sv_P3"
        }
        self.assertEqual(lookup, expected_lookup)

    def test_parse_flow_logs(self):
        lookup = load_lookup(self.temp_lookup.name)
        tag_counts, port_proto_counts = parse_flow_logs(self.temp_flow.name, lookup)

        expected_tag_counts = {
            "sv_P2": 1,
            "Untagged": 1,
            "sv_P1": 1
        }
        expected_port_proto_counts = {
            ("443", "tcp"): 1,
            ("1024", "tcp"): 1,
            ("23", "tcp"): 1
        }

        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_proto_counts, expected_port_proto_counts)

    def test_output_results(self):
        tag_counts = {
            "sv_P2": 1,
            "Untagged": 2,
            "sv_P1": 3
        }
        port_proto_counts = {
            ("80", "tcp"): 1,
            ("443", "tcp"): 1,
            ("1024", "tcp"): 1
        }
        
        captured_output = StringIO()
        sys.stdout = captured_output
        output_results(tag_counts, port_proto_counts)
        sys.stdout = sys.__stdout__
        
        expected_output = (
            "Tag Counts:\n"
            "Tag,Count\n"
            "Untagged,2\n"
            "sv_P1,3\n"
            "sv_P2,1\n"
            "\n"
            "Port/Protocol Combination Counts:\n"
            "Port,Protocol,Count\n"
            "80,tcp,1\n"
            "443,tcp,1\n"
            "1024,tcp,1\n"
        )
        self.assertEqual(captured_output.getvalue(), expected_output)



if __name__ == "__main__":
    unittest.main()

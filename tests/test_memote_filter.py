import unittest
import sys
import os

# Add the parent directory to the path so it can find memote_filter.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memote_filter import extract_actionable_errors

class TestMemoteFilter(unittest.TestCase):
    def test_smart_truncation(self):
        """
        Proves that if a MEMOTE report has hundreds of failed reactions,
        the filter successfully truncates them to protect the LLM context window.
        """
        mock_report = {
            "tests": {
                "test_massive_failure": {
                    "title": "Mass Balance",
                    "summary": "Many reactions failed.",
                    "result": "Failed",
                    "metric": 0.0,
                    # Simulating 6 failing reactions
                    "data": ["rxn1", "rxn2", "rxn3", "rxn4", "rxn5", "rxn6"] 
                }
            }
        }
        
        # Run the extraction with a max of 5 items
        results = extract_actionable_errors(mock_report, max_items=5)
        
        # 1. Check that it found the error
        self.assertEqual(len(results), 1)
        
        affected = results[0]["affected_items"]
        
        # 2. Check that it capped the list at 5 items + 1 warning message = 6 total elements
        self.assertEqual(len(affected), 6)
        
        # 3. Check that the semantic hint to use graph queries is injected
        self.assertIn("...and 1 more items. (Use specific graph queries", affected[-1])

if __name__ == '__main__':
    unittest.main()
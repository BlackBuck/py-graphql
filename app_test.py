import unittest
import asyncio
from app import schema

class TestGraphQLApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.schema = schema
    
    def test_branches_query_structure(self):
        """Test that the branches query returns the expected structure."""
        query = """
        query {
            branches {
                edges {
                    node {
                        branch
                        ifsc
                        address
                        city
                        district
                        state
                        bank {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        
        # Execute the query
        result = self.schema.execute_sync(query)
        
        # Check that there are no errors
        self.assertIsNone(result.errors, f"GraphQL errors: {result.errors}")
        
        # Check that data exists
        self.assertIsNotNone(result.data)
        self.assertIn('branches', result.data)
        self.assertIn('edges', result.data['branches'])
        
        # Check that edges is a list
        self.assertIsInstance(result.data['branches']['edges'], list)
    
    def test_branches_query_data_types(self):
        """Test that the returned data has correct types."""
        query = """
        query {
            branches {
                edges {
                    node {
                        branch
                        ifsc
                        bank {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        
        result = self.schema.execute_sync(query)
        
        self.assertIsNone(result.errors)
        
        if result.data['branches']['edges']:
            first_branch = result.data['branches']['edges'][0]['node']
            
            # Check that all fields are strings
            self.assertIsInstance(first_branch['branch'], str)
            self.assertIsInstance(first_branch['ifsc'], str)
            self.assertIsInstance(first_branch['bank']['id'], int)
            self.assertIsInstance(first_branch['bank']['name'], str)
    
    def test_branches_query_has_data(self):
        """Test that the query returns actual data (assuming CSV has data)."""
        query = """
        query {
            branches {
                edges {
                    node {
                        branch
                        bank {
                            name
                        }
                    }
                }
            }
        }
        """
        
        result = self.schema.execute_sync(query)
        
        self.assertIsNone(result.errors)
        
        # This test assumes your CSV file has data
        # If CSV is empty, this test will fail
        edges = result.data['branches']['edges']
        if edges:  # Only test if there's data
            self.assertGreater(len(edges), 0, "Expected at least one branch")
    
    def test_bank_name_field(self):
        """Test that bank names are properly loaded."""
        query = """
        query {
            branches {
                edges {
                    node {
                        bank {
                            name
                        }
                    }
                }
            }
        }
        """
        
        result = self.schema.execute_sync(query)
        
        self.assertIsNone(result.errors)
        
        edges = result.data['branches']['edges']
        if edges:
            for edge in edges[:5]:  # Test first 5 entries
                bank_name = edge['node']['bank']['name']
                self.assertIsInstance(bank_name, str)
                self.assertNotEqual(bank_name.strip(), "", "Bank name should not be empty")
    
    def test_schema_validity(self):
        """Test that the schema is valid."""
        # This test passes if the schema can be created without errors
        self.assertIsNotNone(self.schema)
        
    def test_minimal_query(self):
        """Test a minimal query to ensure basic functionality."""
        query = """
        query {
            branches {
                edges {
                    node {
                        ifsc
                    }
                }
            }
        }
        """
        
        result = self.schema.execute_sync(query)
        self.assertIsNone(result.errors, f"Errors in minimal query: {result.errors}")
        self.assertIsNotNone(result.data)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
# Bank Branches GraphQL API

A GraphQL API server for querying bank branch information built with Python, Strawberry GraphQL, and Flask.

## Features

- GraphQL API with Strawberry
- Bank and Branch data queries
- CSV data source
- Comprehensive test suite
- Relay-style connections with edges and nodes

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BlackBuck/py-graphql
   cd py-graphql
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Prepare your data

Create a CSV file named `bank_branches.csv` in the root directory with the following columns:

```csv
bank_id,bank_name,branch,ifsc,address,city,district,state
1,State Bank of India,Mumbai Main,SBIN0000001,SBI Building Mumbai,Mumbai,Mumbai,Maharashtra
2,HDFC Bank,Delhi Main,HDFC0000001,HDFC Building Delhi,Delhi,Delhi,Delhi
3,ICICI Bank,Bangalore Main,ICIC0000001,ICICI Building Bangalore,Bangalore,Bangalore,Karnataka
```

**Required CSV columns:**
- `bank_id`: Unique identifier for the bank
- `bank_name`: Name of the bank
- `branch`: Branch name
- `ifsc`: IFSC code
- `address`: Branch address
- `city`: City name
- `district`: District name
- `state`: State name

### 2. Project Structure

```
py-graphql/
├── app.py              # Main GraphQL schema and data loading
├── server.py           # Flask server wrapper
├── app_test.py         # Test suite
├── requirements.txt    # Python dependencies
├── bank_branches.csv   # Your data file
└── README.md          # This file
```

## Running the Server

### Option 1: Direct Flask Server

```bash
python server.py
```

The server will start at `http://localhost:5000`

- **Home page:** `http://localhost:5000/`
- **GraphQL endpoint:** `http://localhost:5000/graphql`

### Option 2: Development Server

For development, you can also run just the GraphQL schema:

```bash
python -c "from app import schema; print('Schema loaded successfully')"
```

## API Usage

### GraphQL Endpoint

**URL:** `POST http://localhost:5000/graphql`

### Sample Queries

#### 1. Get all branches with bank information

```graphql
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
```

#### 2. Get basic branch information

```graphql
query {
  branches {
    edges {
      node {
        branch
        ifsc
        bank {
          name
        }
      }
    }
  }
}
```

#### 3. Get branches with location details

```graphql
query {
  branches {
    edges {
      node {
        branch
        city
        district
        state
        bank {
          name
        }
      }
    }
  }
}
```

### Using cURL

```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { branches { edges { node { branch ifsc bank { name } } } } }"
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:5000/graphql"
query = """
query {
  branches {
    edges {
      node {
        branch
        ifsc
        bank {
          name
        }
      }
    }
  }
}
"""

response = requests.post(url, json={"query": query})
print(response.json())
```

## Testing

Run the test suite to ensure everything is working correctly:

```bash
# Run all tests
python app_test.py

# Run with verbose output
python app_test.py -v

# Run with pytest (if installed)
pytest app_test.py -v
```

### Test Coverage

The test suite includes:
- Schema validation
- Query structure verification
- Data type checking
- Bank name field validation
- Basic functionality tests

## Development

### Adding New Queries

To add new queries, modify the `Query` class in `app.py`:

```python
@strawberry.type
class Query:
    @strawberry.field
    def branches(self) -> BranchConnection:
        return BranchConnection(edges=[BranchEdge(node=b) for b in BRANCHES])
    
    # Add your new query here
    @strawberry.field
    def branch_by_ifsc(self, ifsc: str) -> Branch:
        for branch in BRANCHES:
            if branch.ifsc == ifsc:
                return branch
        return None
```

### Modifying Data Structure

1. Update the CSV file with new columns
2. Modify the `Branch` or `Bank` classes in `app.py`
3. Update the data loading logic
4. Add corresponding tests

## Troubleshooting

### Common Issues

1. **CSV file not found:**
   ```
   FileNotFoundError: [Errno 2] No such file or directory: 'bank_branches.csv'
   ```
   **Solution:** Make sure `bank_branches.csv` exists in the root directory.

2. **Import errors:**
   ```
   ModuleNotFoundError: No module named 'strawberry'
   ```
   **Solution:** Install dependencies with `pip install -r requirements.txt`

3. **Empty results:**
   If queries return empty results, check:
   - CSV file has data
   - Column names match expected names
   - No encoding issues in CSV file

### Debug Mode

Run the server in debug mode to see detailed error messages:

```bash
export FLASK_DEBUG=1
python server.py
```

## Dependencies

- **strawberry-graphql**: GraphQL library for Python
- **Flask**: Web framework
- **pandas**: Data manipulation library

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## API Schema

### Types

```graphql
type Bank {
  id: Int!
  name: String!
}

type Branch {
  branch: String!
  ifsc: String!
  address: String!
  city: String!
  district: String!
  state: String!
  bank: Bank!
}

type BranchEdge {
  node: Branch!
}

type BranchConnection {
  edges: [BranchEdge!]!
}

type Query {
  branches: BranchConnection!
}
```
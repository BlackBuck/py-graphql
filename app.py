import strawberry
from typing import List
import pandas as pd

@strawberry.type
class Bank:
    id: int
    name: str

@strawberry.type
class Branch:
    branch: str
    ifsc: str
    address: str
    city: str
    district: str
    state: str
    bank: Bank

# Load bank branches data from a CSV file
df = pd.read_csv("bank_branches.csv", encoding="utf-8")

# Extract unique banks from the DataFrame
BANKS = []
bank_name_to_obj = {}
for idx, bank_name in enumerate(df['bank_name'].unique(), start=1):
    bank_id = df[df['bank_name'] == bank_name]['bank_id'].iloc[0]
    bank_obj = Bank(id=str(bank_id), name=bank_name)
    BANKS.append(bank_obj)
    bank_name_to_obj[bank_name] = bank_obj

# Create Branch objects from DataFrame
BRANCHES = []
for i, row in df.iterrows():
    bank_obj = bank_name_to_obj.get(row['bank_name'])
    branch_obj = Branch(
        branch=str(row['branch']) if pd.notna(row['branch']) else "",
        ifsc=str(row['ifsc']) if pd.notna(row['ifsc']) else "",
        address=str(row['address']) if pd.notna(row['address']) else "",
        city=str(row['city']) if pd.notna(row['city']) else "",
        district=str(row['district']) if pd.notna(row['district']) else "",
        state=str(row['state']) if pd.notna(row['state']) else "",
        bank=bank_obj,
    )
    BRANCHES.append(branch_obj)

# print(BANKS)

@strawberry.type
class BranchEdge:
    node: Branch

@strawberry.type
class BranchConnection:
    edges: List[BranchEdge]

@strawberry.type
class Query:
    @strawberry.field
    def branches(self) -> BranchConnection:
        return BranchConnection(edges=[BranchEdge(node=b) for b in BRANCHES])

schema = strawberry.Schema(query=Query)
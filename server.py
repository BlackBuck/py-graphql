from flask import Flask
from strawberry.flask.views import GraphQLView
from app import schema
import os

app = Flask(__name__)

# Add GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

# Add a simple root endpoint
@app.route('/')
def home():
    return '''
    <h1>Bank Branches GraphQL API</h1>
    <p>Visit <a href="/graphql">/graphql</a> for GraphQL endpoint</p>
    <p>Example query:</p>
    <pre>
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
    </pre>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
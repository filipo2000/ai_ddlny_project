import os
from flask import Flask, render_template, request
import openai
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

#THIS FILE CREATES THE UI AND DOES ENGLISH TO SQL CONVERSION

# Load environment variables
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# PostgreSQL connection
DB_ENGINE = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

# Initialize Flask app
app = Flask(__name__)

# GPT function to convert English to SQL
def english_to_sql_gpt(english_query: str, table_name: str = "products") -> str:
    prompt = f"""
Convert the following English request into a valid SQL query for a PostgreSQL table called "{table_name}".
Only provide the SQL code, no explanation.

Request: "{english_query}"
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only outputs SQL code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql_code = response.choices[0].message.content.strip()
    if sql_code.startswith("```"):
        sql_code = "\n".join(sql_code.split("\n")[1:-1])
    return sql_code

# Flask route for homepage
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None

    if request.method == "POST":
        english_query = request.form.get("english_query", "")
        if english_query:
            try:
                # Convert English to SQL
                sql_query = english_to_sql_gpt(english_query)
                
                # Execute the SQL query
                with DB_ENGINE.connect() as conn:
                    result_proxy = conn.execute(text(sql_query))
                    result = [dict(row) for row in result_proxy.mappings()]
            except Exception as e:
                error_message = str(e)

    return render_template(
        "index.html",
        result=result,
        error_message=error_message
    )

if __name__ == "__main__":
    app.run(debug=True)

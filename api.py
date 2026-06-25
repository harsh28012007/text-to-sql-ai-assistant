from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI()

engine = create_engine("sqlite:///./amazon.db")

class Query(BaseModel):
    question: str

def generate_sql(question):
    q = question.lower()

    if "category" in q:
        return """
        SELECT category, COUNT(*) as count
        FROM amazon
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
        """

    elif "total" in q:
        return """
        SELECT category, SUM(discounted_price) as total
        FROM amazon
        GROUP BY category
        ORDER BY total DESC
        LIMIT 10
        """

    elif "rating" in q:
        return """
        SELECT category, AVG(rating) as avg_rating
        FROM amazon
        GROUP BY category
        ORDER BY avg_rating DESC
        LIMIT 10
        """

    elif "top" in q:
        return """
        SELECT product_name, discounted_price
        FROM amazon
        ORDER BY discounted_price DESC
        LIMIT 5
        """

    elif "cheap" in q or "lowest" in q:
        return """
        SELECT product_name, discounted_price
        FROM amazon
        ORDER BY discounted_price ASC
        LIMIT 5
        """

    elif "all" in q:
        return "SELECT * FROM amazon LIMIT 50"

    else:
        return """
        SELECT category, COUNT(*) as count
        FROM amazon
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
        """

@app.post("/query")
def run_query(data: Query):
    sql = generate_sql(data.question)

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        return {
            "sql": sql,
            "data": df.to_dict()
        }

    except Exception as e:
        return {"error": str(e)}
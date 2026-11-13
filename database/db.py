
import sqlite3


def connect_db():
    connection = sqlite3.connect("research.db")
    return connection

def create_table():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            report TEXT NOT NULL,
            total_sources INTEGER,
            structure_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()

def save_research(topic, report, total_sources, structure_score):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO research_history
        (topic, report, total_sources, structure_score)
        VALUES (?, ?, ?, ?)
    """, (topic, report, total_sources, structure_score))

    connection.commit()

    connection.close()

    print("Research report saved successfully!")


def get_all_research():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM research_history
        ORDER BY created_at DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records

if __name__ == "__main__":

    create_table()

    save_research(
        "Generative AI",
        "This is a sample research report.",
        5,
        85.7
    )

    records = get_all_research()

    print("\nResearch History:")

    for record in records:
        print(record)

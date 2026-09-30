import logging
import os
import matplotlib.pyplot as plt
import mysql.connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Read DB credentials from environment variables
DBHOST = os.getenv("DBHOST")
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBNAME = os.getenv("DBNAME")


def get_connection():

    return mysql.connector.connect(
        host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
    )


def get_data_by_group(value):

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM mock WHERE `group` = %s"  # %s is a placeholder
        cursor.execute(query, (value,))  # tuple
        rows = cursor.fetchall()
        logging.info("Fetched %d rows for group %s", len(rows), value)
        return rows
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def plot_counts(groupby):

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM mock")
        valid_cols = [c[0] for c in cursor.fetchall()]
        if groupby not in valid_cols:
            logging.error("Invalid column: %s", groupby)
            return {}

        cursor.execute(
            f"SELECT `{groupby}`, COUNT(*) FROM mock GROUP BY `{groupby}`"
        )
        counts = dict(cursor.fetchall())
        logging.info("Counts by %s: %s", groupby, counts)

        # Bar chart of counts
        plt.bar([str(k) for k in counts], list(counts.values()))
        plt.xlabel(groupby)
        plt.ylabel("count")
        plt.title(f"Rows per {groupby}")
        plt.savefig(f"counts_by_{groupby}.png")
        return counts
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def main():
    rows = get_data_by_group("A")  # change "A" to one of your group values
    print(f"Rows in group A: {len(rows)}")
    for row in rows[:5]:
        print(row)
    print(plot_counts("group"))


if __name__ == "__main__":
    main()
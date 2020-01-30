import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql
import statistics
from time import time

# Connection string info
db = {
    'HOST': 'localhost',
    'PORT': '1283',
    'NAME': 'postgres',
    'USER': 'postgres'
}


def query_db(query):
    str_conn = f"dbname='{db['NAME']}' user='{db['USER']}' host='{db['HOST']}' port='{db['PORT']}'"

    try:
        conn = pg.connect(str_conn)
        cur = conn.cursor()        
    except:
        print("Cannot connect to database.")

    cur.execute(query)
    conn.commit()

# Create table cards

query_db("CREATE TABLE cards(number varchar, suit varchar)")
print("Created table cards!")
# Insert data into the table 

suit = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
N = 50000
numbers = []
suits = []
for s in suit:
    for i in range(1,N+1):
        numbers.append(str(i))
        suits.append(s)

df = pd.DataFrame({'number':numbers, 'suit':suits})
df['values'] = "('" + df['number'] + "', '" + df['suit'] + "')" 
df = df.sample(frac = 1).reset_index(drop = True)
cards = ",\n".join(list(df['values']))

query = f"""INSERT INTO cards VALUES {cards};"""
query_db(query)
print("Data inserted in the table . . .")

def mean_query():
    try:
        str_conn = f"dbname='{db['NAME']}' user='{db['USER']}' host='{db['HOST']}' port='{db['PORT']}'"
        conn = pg.connect(str_conn)
        cur = conn.cursor()        
    except:
        print("Cannot connect to database.")

    t = []
    for _ in range(200):
        start = time()
        # query = """SELECT * FROM cards WHERE number = '100' AND suit = 'Clubs'"""
        query = """SELECT * FROM cards WHERE number = '100'"""
        df = psql.read_sql(query, conn)
        end = time() - start
        t.append(end)
    return statistics.mean(t)


before = mean_query()

# Indexing
# query = """CREATE INDEX col ON cards(suit);"""
query = """CREATE INDEX unq_card ON cards(number, suit);"""
# query = """CREATE INDEX num ON cards(number);"""
query_db(query)

after = mean_query()

print(f"Average time for query BEFORE indexing: {before}")
print(f"Average time for query AFTER indexing {after}")    
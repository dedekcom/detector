import psycopg2

try:
    conn = psycopg2.connect("dbname='portfolio' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute("""select * from financial_reports f, market_goods g where f."GoodId" = g."Id" """)
    rows = cur.fetchall()
    print rows[0]
except:
    print "I am unable to connect to the database"

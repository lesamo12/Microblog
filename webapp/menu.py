from mysql.connector import connection
def bd():
    cnx= connection.MySQLConnection(user='root', password='',
                                    host='127.0.0.1', database='annuaire')
    cursor=cnx.cursor()
    data = ("Select * from personne ")
    cursor.execute(data)
    liste = cursor.fetchall()

    return  liste

if __name__ == "__main__":
    x=bd()
    print(x)
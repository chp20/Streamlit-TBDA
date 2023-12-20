import 
connection = mysql.connector.connect(
        host="apiivm78.etsii.upm.es",
        user="TBDA",
        password="UPM#2324",
        database="sclerosisTBDA"
    )

    checkdata = []
    mycursor = connection.cursor()
    qry = "select * FROM `Data_sample_Christian`"
    mycursor.execute(qry)
    rows = mycursor.fetchall()

    for x in rows:
        if final_date_begin <= x[1] and final_date_end >= x[2]:
            checkdata.append(x)

    mycursor.close()
    connection.close()

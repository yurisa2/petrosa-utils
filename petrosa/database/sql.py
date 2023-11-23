import logging
import os
import pkg_resources

import mysql.connector


ver = pkg_resources.get_distribution("petrosa").version
logging.info("petrosa-utils version: " + ver)


def connect_mysql():
    cnx = mysql.connector.connect(
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_SERVER"),
        database=os.getenv("MYSQL_DB"),
        connection_timeout=30,
    )

    cursor = cnx.cursor(buffered=True, dictionary=True)

    return cnx, cursor


def build_sql(record_list, table, mode="REPLACE") -> str:
    sql = f"{mode} INTO `{table}` ("

    keys = record_list[0].keys()

    for key in keys:
        sql += "`" + key + "`, \n"
    sql = sql[:-3]

    sql += ") VALUES "

    for record in record_list:
        sql += "("
        for key in keys:
            if str(record[key]).lower() in ["nan", "inf"]:
                sql += "NULL"
            else:
                sql += '"' + str(record[key]) + '"'

            sql += ", "

        sql = sql[:-2]
        sql += "), "

    sql = sql[:-2]

    return sql


def update_sql(record_list: list, table: str, mode="REPLACE"):
    logging.info(f"Inserting {len(record_list)} records on {table}")
    cnx, cursor = connect_mysql()
    sql = build_sql(record_list, table, mode)

    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()


def run_generic_sql(sql_str):
    logging.info(f"Running Generic SQL {sql_str}")
    cnx, cursor = connect_mysql()

    cursor.execute(sql_str)
    if(sql_str[:6] == "SELECT" or sql_str[:6] == "select" or sql_str[:6] == "Select"):
        logging.info("Returning rows")
        rows = cursor.fetchall()
    else:
        logging.info("Returning None")
        rows = None
    cnx.commit()
    cursor.close()
    cnx.close()

    return rows
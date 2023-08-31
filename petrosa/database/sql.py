import logging
import os

import mysql.connector


def connect_mysql():
    cnx = mysql.connector.connect(user=os.getenv("MYSQL_CRYPTO_USER"),
                                  password=os.getenv(
        "MYSQL_CRYPTO_PASSWORD"),
        host=os.getenv(
        "MYSQL_CRYPTO_SERVER"),
        database=os.getenv(
        "MYSQL_CRYPTO_DB"),
        connection_timeout=30
    )

    cursor = cnx.cursor(buffered=True)

    return cnx, cursor


def build_sql(record_list: list, table: str, mode="REPLACE") -> str:

    sql = f"{mode} INTO `{table}` ("

    keys = record_list[0].keys()

    for key in keys:
        sql += "`" + key + "`, \n"
    sql = sql[:-3]

    sql += ") VALUES "

    for record in record_list:
        sql += "("
        for key in keys:
            if (str(record[key]).lower() in ["nan", "inf"]):
                sql += "NULL"
            else:
                sql += '"' + str(record[key]) + '"'

            sql += ", "

        sql = sql[:-2]
        sql += "), "

    sql = sql[:-2]

    return sql


def update_sql(record_list: list[dict], table: str, mode="REPLACE"):

    logging.info(f"Inserting {len(record_list)} records on {table}")
    cnx, cursor = connect_mysql()
    sql = build_sql(record_list, table, mode)

    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()

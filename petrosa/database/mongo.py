import os

import pandas as pd
import pymongo


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:mopMuXDvZL@localhost:27017'),
        readPreference='secondaryPreferred',
        appname=os.getenv("OTEL_SERVICE_NAME", "no-name-from-utils")
    )

    return client


def get_data(mongo_db, col_name, ticker, limit=999999999):

    client = get_client()
    db = client[mongo_db]
    history = db[col_name]

    results = history.find({'ticker': ticker},
                           sort=[('datetime', -1)]).limit(limit)
    results_list = list(results)

    if (len(results_list) == 0):
        return []

    data_df = pd.DataFrame(results_list)

    data_df = data_df.sort_values("datetime")

    data_df = data_df.rename(columns={"open": "Open",
                                      "high": "High",
                                      "low": "Low",
                                      "close": "Close"}
                             )

    data_df = data_df.set_index('datetime')

    return data_df


def post_results(mongo_db, symbol, test_period, doc, strategy):
    client = get_client()
    db = client[mongo_db]
    col = db['backtest_results']
    col.delete_one({"strategy": strategy,
                                                          "symbol": symbol,
                                                          "period": test_period
                                                          })
    col.update_one(
        {"strategy": strategy,
         "symbol": symbol,
         "period": test_period
         }, {"$set": doc}, upsert=True)
    return True


def post_list_results(mongo_db, symbol, test_period, doc, strategy):
    client = get_client()
    db = client[mongo_db]
    col = db['backtest_results_lists']
    col.delete_one({"strategy": strategy,
                                                                "symbol": symbol,
                                                                "period": test_period
                                                                })

    col.update_one(
        {"strategy": strategy,
         "symbol": symbol,
         "period": test_period
         }, {"$set": doc}, upsert=True)
    return True

import datetime
import pandas as pd

def remove_weird_chars(results):
    # results_json = json.loads(json.dumps(results.to_dict(), default=str))
    results_json = results

    new_res = {}

    for key in results_json.keys():
        old_key = key
        new_key = old_key.replace('.', '_')
        new_key = new_key.replace(' ', '_')
        new_key = new_key.replace('%', 'pcent')
        new_key = new_key.replace('[', '')
        new_key = new_key.replace(']', '')
        new_key = new_key.replace('(', '')
        new_key = new_key.replace(')', '')
        new_key = new_key.replace('$', '')
        new_key = new_key.replace('&', 'and')
        new_key = new_key.replace('#', 'n')
        new_key = new_key.replace('__', '_')
        new_key = new_key.lower()

        new_res[new_key] = results_json[old_key]

    return new_res

def dict_time_convert(stats):
    from datetime import timedelta
    ret_res = {}
    
    for key in stats.keys():
        if isinstance(stats[key], pd.Timedelta):
            ret_res[key] = stats[key].total_seconds()
        elif isinstance(stats[key], pd.Timestamp):
            ret_res[key] = stats[key].to_pydatetime()
        else:
            ret_res[key] = stats[key]

    return ret_res

def result_maker(stats, params, test_params, test_type):
    if '_trades' in stats:
        del(stats['_trades'])
    if '_strategy' in stats:
        del(stats['_strategy'])
    if '_equity_curve' in stats:
        del(stats['_equity_curve'])
        
    if '_id' in test_params:
        del(test_params["_id"])

    stats = remove_weird_chars(stats)
    params = remove_weird_chars(params)

    stats = dict_time_convert(stats)
    
    ret = {**test_params, **stats, **params}
    ret['test_type'] = test_type
    ret['insert_timestamp'] = datetime.datetime.now()
        
    return ret


def list_maker(stats, test_params):
    list_doc = {}
    list_doc['insert_timestamp'] = datetime.datetime.now()
    list_doc['n_trades'] = stats['# Trades']
    list_doc['strategy'] = test_params['strategy']
    list_doc['period'] = test_params['period']
    list_doc['symbol'] = test_params['symbol']
    list_doc['trades_list'] = stats._trades.to_dict('records')

    ret = {**list_doc, **test_params}
    
    return ret
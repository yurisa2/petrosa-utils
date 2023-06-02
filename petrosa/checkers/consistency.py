import datetime


def generate_benchmark_list(start: datetime.datetime, 
                            end: datetime.datetime, 
                            period: str):
    
    if period == '5m' or period == 'm5':
        minutes = 5
    elif period == '15m' or period == 'm15':
        minutes = 15
    elif period == '30m' or period == 'm30':
        minutes = 30
    elif period == '1h' or period == 'h1':
        minutes = 60
    else:
        minutes = 0

    datepointer = start        
    division_list = []
    
    while datepointer <= end:
        if(datepointer.minute % minutes == 0):
            division_list.append(datepointer.replace(second=0, microsecond=0))
        
        datepointer = datepointer + datetime.timedelta(minutes=1)
    
    division_list.pop(-1)
    
    return division_list


def check_consistency(start: datetime.datetime, 
                      end: datetime.datetime, 
                      actual: list , 
                      period: str):
    benchmark = generate_benchmark_list(start, end, period)
    
    lacking = []
    
    for item in benchmark:
        if item not in actual:
            lacking.append(item)
            
    return lacking

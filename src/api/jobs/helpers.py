from datetime import datetime

def convert_string_to_date(str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y-%m-%d').date()
    if str_end_date is not None:
        end_date = datetime.strptime(str_end_date, '%Y-%m-%d').date()
    else:
        end_date = None
    
    return (start_date,end_date)

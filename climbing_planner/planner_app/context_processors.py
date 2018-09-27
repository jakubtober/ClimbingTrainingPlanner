import datetime

def date_processor(request):
    dates_dict = {
        'date_today': datetime.date.today(),
    }
    return dates_dict

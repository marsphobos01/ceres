import datetime

class DateMaths():
    @staticmethod
    def get_calendar_range(view_type: str, anchor_date: str):
        anchor_date = datetime.datetime.strftime(anchor_date, "%Y/%M/%d")
        match view_type:
            case "day":
                range_end = datetime.datetime.strptime(anchor_date,"%Y/%M/%d") + datetime.timedelta(days=1)
                return (anchor_date, range_end)
            case "month":
                range_end = datetime.datetime.strptime(anchor_date, "%Y/%M/%d") + datetime.timedelta(months=1)
                return (anchor_date, range_end)
            case "year":
                range_end = datetime.datetime.strptime(anchor_date, "%Y/%M/%d") + datetime.timedelta(days=365)
                return (anchor_date, range_end.strftime("%Y/%M/%dd"))




        return (range_start, range_end)



print(DateMaths.get_calendar_range("day", datetime.datetime.now()))



























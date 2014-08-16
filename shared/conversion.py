def datetime_to_json(dt):
    if dt is None:
        return None
    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.timetuple().tm_hour,
        'minute': dt.timetuple().tm_min,
        'second': dt.timetuple().tm_sec,
        'timezone': get_timezone_info(dt)
    }


def get_timezone_info(dt):
    if not hasattr(dt, 'tzinfo'):
        return None
    if not hasattr(dt.tzinfo, 'tzname'):
        return None
    return dt.tzinfo.tzname(dt)

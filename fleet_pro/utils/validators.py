def validate_not_empty(value):
    return bool(value and str(value).strip())

def validate_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_year(value):
    try:
        year = int(value)
        return 1900 <= year <= 2100
    except ValueError:
        return False

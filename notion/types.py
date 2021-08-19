from datetime import date

FILTERS = {
    'type': lambda t: {
        "property": "Type",
        "select": {
            "equals": t,
        }
    } if t else {
        "property": "Type",
        "select": {
            "is_empty": True
        }
    },
    'complete': lambda complete=False: {
        "property": "Done",
        "checkbox": {
            "equals": complete,
        }
    }
}

SORTS = {
    'created': lambda direction='ascending': {
        "property": "Created",
        "direction": direction,
    },
    'due': lambda direction='descending': {
        "property": "Due",
        "direction": direction,
    }
}


class DateProperty:
    start = None
    end = None

    def __init__(self, property_data):
        for k, v in property_data['date'].items():
            if v:
                setattr(self, k, date.fromisoformat(v))


class TextPropterty:
    def __init__(self):
        pass


class DueDate(DateProperty):
    def is_due(self):
        return self.start <= date.today()

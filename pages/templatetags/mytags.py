import json

from django import template

register = template.Library()

@register.filter
def loadjson(data):
    if data:
        print(json.loads(data))
        days = []
        string = ''
        for year in json.loads(data):
            string += f'Год {year} . '
            print(year)
            for month in json.loads(data)[year]:
                print(month)
                string += f'Месяц {month} Числа: '
                for day in json.loads(data)[year][month]:
                    string += f'{day} '
                    print (day)
            days.append(string)
        return days


@register.simple_tag
def get_chat_user(data,curUser):
    print(curUser)
    print(data.users.all().exclude(curUser))
    return
import openaq_py



def data_grab(city, parameter):
    """Basic fucntion to get the base data"""
    api = openaq_py.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    li = [(i['date']['utc'], i['value']) for i in body['results']]
    return li

def drop_downs():
    api = openaq_py.OpenAQ()
    stat1, body1 = api.cities()
    cities = [(i['city'],i['city'].replace(' ',"8")) for i in body1['results']]
    stat2, body2 = api.parameters()
    parameters = [(i['name'],i['description'],i['id']) for i in body2['results']]
    return(cities,parameters)

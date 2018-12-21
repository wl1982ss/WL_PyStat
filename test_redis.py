import redis


class Database:
    def __init__(self):
        self.host = '192.168.1.107'
        self.port = 6379

    def write(self, website, city, year, month, day, deal_number):
        try:
            key = '_'.join([website, city, str(year), str(month), str(day)])
            val = deal_number
            r = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
            r.set(key, val)
        except Exception as exception:
            print(exception)

    def read(self, website, city, year, month, day):
        try:
            key = '_'.join([website, city, str(year), str(month), str(day)])
            r = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
            value = r.get(key)
            print(value)
            return value
        except Exception as exception:
            print(exception)


if __name__ == '__main__':
    db = Database()
    db.write('meituan', 'beijing', 2013, 9, 1, 8000)
    db.read('meituan', 'beijing', 2013, 9, 1)

"""
r = redis.Redis(host='192.168.1.107', port=6379, decode_responses=True)
r.set('name', 'junxi')
print(r['name'])
print(r.get('name'))
print(type(r.get('name')))
"""
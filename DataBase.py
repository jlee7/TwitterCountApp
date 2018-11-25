"""
Database with peewee
"""
from peewee import *
from datetime import datetime


db = SqliteDatabase('TwitterCount.db')

class Entry(Model):
    keyword = CharField()
    address = CharField()
    coordinates = CharField()
    radius = CharField()
    date = CharField()
    count = IntegerField()

    class Meta:
        database = db


def add_entry(kw, adrs, coords, rds, cnt):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Entry.create(keyword = kw,
                 address = adrs,
                 coordinates = coords,
                 radius = rds,
                 date = dt,
                 count = cnt).save()

    print('Database has been updated: {}, {}, {}, {}, {}, {}'.format(kw,
                                                                    adrs,
                                                                    coords,
                                                                    rds,
                                                                    dt,
                                                                    cnt))


def get_entry(kw):
    return Entry.get(Entry.keyword == kw)


def get_all_entries():

    results = dict()

    for item in Entry.select():
        results[item.get_id()] = {"keyword": str(item.keyword),
                                "address": str(item.address),
                                "coordinates": str(item.coordinates),
                                "radius": str(item.radius),
                                "date": str(item.date),
                                "count": str(item.count)}
    
    print("id:", type(item.get_id()))
    print("keyword:", type(item.keyword))
    print("address:", type(item.address))
    print("coordinates:", type(item.coordinates))
    print("radius:", type(item.radius))
    print("date:", type(item.date))
    print("count:", type(item.count))

    print(results)

    return results


if __name__ == "__main__":
    print('Database module')

    db.connect()
    db.create_tables([Entry])

    # entry_one = Entry(keyword = "Schwebebahn",
    #                   address = "Friedrich-Engels-Allee 22, 42208, Wuppertal",
    #                   coordinates = '51.270086, 7.191741',
    #                   radius = "5",
    #                   date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                   count = 345)
    # entry_one.save()


    for n in Entry.select():
        print(n.keyword)


    print(get_all_entries())
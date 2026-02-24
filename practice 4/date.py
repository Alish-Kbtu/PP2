import datetime

print(datetime.date.today() - datetime.timedelta(days = 5))

t = datetime.date.today()
print(t - datetime.timedelta(days = 1))
print(t)
print(t + datetime.timedelta(days = 1))

n = datetime.datetime.now()
print(n.replace(microsecond = 0))

d1 = datetime.datetime(2024, 7, 24, 10, 0, 0)
d2 = datetime.datetime(2024, 7, 18, 12, 30, 0)
d = d1 - d2
print(d.total_seconds())
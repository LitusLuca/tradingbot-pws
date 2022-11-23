file = input("file to reorganize: ")
old = open(file).read()
new = open(file, 'w')

old = old.split('\n')
for day in old:
    if day != old[0]:
        new.write('\n')
    day = day.replace('$','')
    day = day.split(',')
    date = day[0]
    date = date.replace('/', '-')
    date = date.split('-')
    date = date[2]+'-'+date[0]+'-'+date[1]
    day = date+','+day[3]+','+day[4]+','+day[5]+','+day[1]+','+day[2]
    new.write(day)


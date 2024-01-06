import datetime

# Get the current date and time
d = str(datetime.datetime.now().day)
m = str(datetime.datetime.now().month)
y = str(datetime.datetime.now().year)
h = str(datetime.datetime.now().hour)
mn = str(datetime.datetime.now().minute)
# s= datetime.now().second
# mm = datetime.now().microsecond
noww =y+'-'+ m +'-'+d +' '+'in'+ ' ' +h+':' +mn
# Print the current date and time
print("Current date and time: ", noww)
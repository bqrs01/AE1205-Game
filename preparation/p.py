"""
2:29
5:58
10:10
15:28
19:57
23:09
26:46
29:35
31:40
37:57
41:28
"""
lst = []
a = "12:45"

while True:
    try:
        a = input("")
        mins, secs = a.split(":")
        mins = int(mins)
        secs = int(secs)
        lst.append((mins*60) + secs)
    except:
        break

print(lst)

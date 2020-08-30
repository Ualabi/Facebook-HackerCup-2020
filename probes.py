total, past = 1, 0
for x in range(1,100):
    past += x
    total *= past
print(total)
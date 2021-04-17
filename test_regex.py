import re


#pattern = "\D\d\D\d"
pattern = "[a-hA-H][1-8][a-hA-H][1-8]"

while True:
    user_input = input()
    if(re.search(pattern,user_input)):
        print(re.findall(pattern,user_input)[0])
    else:
        print("Invalid move")




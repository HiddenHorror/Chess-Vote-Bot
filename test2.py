#Test Api from https://python-lichess.readthedocs.io/en/latest/api.html
#Python chess https://github.com/niklasf/python-chess
#Beserk https://github.com/rhgrant10/berserk
#import threading

fname = "User_IDs.txt"
lichess_users = []
twitch_users = []

with open("User_IDs.txt", "r") as f:
    next(f)
    for line in f:
        lichess_users.append(line.split(",")[0].strip())
        twitch_users.append(line.split(",")[1].strip())
    f.close()
# my_file = open("User_IDs.txt", "r")
# content_list = my_file.read().splitlines()
# my_file.close()
# lichess_users = []
# twitch_users = []
#
# for el in content_list:
#     print(el)
#     lichess_users.append(el.split(",")[0].strip())
#     twitch_users.append(el.split(",")[1].strip())
print(lichess_users)
print(twitch_users)



# VALID_LICHESS_USERS = ["a" ,"Zuschauer"]
# VALID_TWITCH_USERS = ["b", "brainlighter"]
# VALID_USERS = list(zip(VALID_LICHESS_USERS, VALID_TWITCH_USERS))
# print(VALID_USERS)
#
# if "Zuschauer" in VALID_LICHESS_USERS:
#     index = VALID_LICHESS_USERS.index("Zuschauer")
#     print(VALID_USERS[index][1])

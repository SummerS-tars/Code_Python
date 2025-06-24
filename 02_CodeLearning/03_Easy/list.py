game_list = ["Minecraft", "Don't Starve"]

print("len(game_list): " + str(len(game_list)))
print(game_list)

print("Add a new game: " + "Stardew Valley")

game_list.append("Stardew Valley")

print("len(game_list): " + str(len(game_list)))
print(game_list)

print("Remove a game: " + "Minecraft")

game_list.remove(game_list[0])

# ! this also works
# game_list.remove("Minecraft")

print("len(game_list): " + str(len(game_list)))
print(game_list)


# ! below procedure also works but not recommended(and it will be linted as error here)
# print("list in Python supports multiple data types")

# print("add 114514(int) to the list")
# game_list.append(114514)

# print("len(game_list): " + str(len(game_list)))
# print(game_list)
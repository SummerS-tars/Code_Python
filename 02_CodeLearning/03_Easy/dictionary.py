meme_dict = { "114514": "1919810",
            "同济大学": "65472"}

print(len(meme_dict))
print(meme_dict)

meme_dict["复旦大学"] = "3.3"

print(len(meme_dict))
print(meme_dict)

meme_dict["复旦大学"] = "3.7"

print(len(meme_dict))
print(meme_dict)

query = input("Enter a key: ")
if query in meme_dict:
    print("the key " + query + " is in the dictionary")
    print(meme_dict[query])
else:
    print("the key " + query + " is not in the dictionary")

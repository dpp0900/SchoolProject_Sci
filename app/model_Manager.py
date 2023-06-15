import json

def appendBlacklist(word):
    wordsData = json.load(open("model.json", "r"))
    wordsData["blacklist"].append(word)
    json.dump(wordsData, open("model.json", "w"), indent=4, ensure_ascii=False)

if __name__ == "__main__":
    while True:
        appendBlacklist(input("word: "))
        print("done")
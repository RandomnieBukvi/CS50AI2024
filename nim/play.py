from nim import train, play

ai = train(10000)

while True:
    play(ai)
    if input("Exit? type y:") == "y":
        break
    print("---------NEW GAME--------")

from elosports.elo import Elo
import time
import random
import mysql.connector

# Elo setup
eloLeague = Elo(k=20, homefield=0)

# Load in sql data base
db = mysql.connector.connect(host="localhost", user="root", password="password", database="bestgirl")

cursor = db.cursor()
cursor.execute("use bestgirl;")
cursor.execute("select * from anime_girls;")
data = {i[0]: i[1::] for i in cursor}

# Load in the elo leages
for i in list(data.keys()):
    eloLeague.addPlayer(i, rating=data[i][1])


def get_image(name):
    global cursor

    cursor.execute(f"select * from links where name = \'{name}\' order by number_picked; ")

    urls = {i[0]: i[1::] for i in cursor}

    picked = list(urls.keys())[0]


    #print( picked)
    print(picked, ":", urls[picked])

    cursor.execute(
        "update links set number_picked = number_picked + 1 where ID = \""
        + str(picked)
        + "\";"
    )
    return urls[picked][1]


async def poll(message):
    # Gives us an updated list
    if message.channel.name == "animemes" and message.content == "who is bestgirl":

        cursor.execute("use bestgirl")
        cursor.execute("select * from anime_girls order by elo desc;")
        data = {i[0]: i[1::] for i in cursor}

        silly = ""
        print(data)
        count = 1
        for i in list(data.keys()):
            silly += str(count) + ") " + str(i) + ": " + str(round(data[i][1], 1)) + "\n"
            count += 1
        await message.channel.send(silly)

    # Block To Rate Anima Girls
    if (
            message.channel.name == "animemes" and message.author.id == 309512449315307530 and message.content == "bestgirl"):
        count = 0

        # Infinite many polls
        while True:

            # Selection process
            cursor.execute("use bestgirl")
            cursor.execute("select * from anime_girls order  by number_matches;")
            data = {i[0]: i[1::] for i in cursor}

            # Select player one by least matches
            p1 = list(data.keys())[0]

            # select player two by distance from player one
            for i in range(5):
                p2 = sorted(data, key=lambda x: abs(data[p1][1] - data[x][1]))[i]

                if p1 != p2:
                    break

            await message.channel.send(
                "\n\n" + "-" * len(p1 + " vs " + p2) + "\n" + p1 + " vs " + p2 + "\n" + "-" * len(
                    p1 + " vs " + p2) + "\n")

            # Reactions to vote
            emoji = '♥️'
            print("sending")
            m1 = await message.channel.send(get_image(p1))
            await m1.add_reaction(emoji)

            m2 = await message.channel.send(get_image(p2))
            await m2.add_reaction(emoji)

            timeout = time.time() + 60 * 60 * 12
            # vote Loop
            while True:
                votes = {i: "" for i in ["Capio", "SquidCat", "Slifyre", "Lary", "Radscorpion", "other"]}
                try:
                    m1 = await message.channel.fetch_message(m1.id)
                except:
                    print("error in m1")

                try:
                    m2 = await message.channel.fetch_message(m2.id)

                except:
                    print("error in m2")

                flag = False
                if m1.reactions[0].count >= 4:
                    eloLeague.gameOver(winner=p1, loser=p2, winnerHome=False)
                    cursor.execute(
                        "update anime_girls set number_wins = number_wins + 1 where contender_name = \""
                        + p1
                        + "\";"
                    )

                    await message.channel.send(p1 + " wins ")

                    print(eloLeague.ratingDict[p1])

                    flag = True

                if m2.reactions[0].count >= 4:
                    eloLeague.gameOver(winner=p2, loser=p1, winnerHome=False)
                    cursor.execute(
                        "update anime_girls set number_wins = number_wins + 1 where contender_name = \"" + p2 + "\";")
                    await message.channel.send(p2 + " wins ")
                    flag = True

                if time.time() > timeout:
                    message.channel.send("Time limit exceed and the round will be nullifyed")
                    break

                if flag:
                    p1_votes = list()
                    p2_votes = list()

                    for i in m1.reactions:
                        async for user in i.users():
                            p1_votes.append(user.name)

                    for i in m2.reactions:
                        async for user in i.users():
                            p2_votes.append(user.name)

                    for i in votes.keys():
                        if i in p1_votes and i not in p2_votes:
                            votes[i] = p1

                        if i in p2_votes and i not in p1_votes:
                            votes[i] = p2

                    # Update all the match info
                    cursor.execute("update anime_girls set elo = " + str(
                        eloLeague.ratingDict[p1]) + " where contender_name = \"" + p1 + "\";")
                    cursor.execute("update anime_girls set elo = " + str(
                        eloLeague.ratingDict[p2]) + " where contender_name = \"" + p2 + "\";")
                    cursor.execute(
                        "update anime_girls set number_matches = number_matches + 1 where contender_name = \""
                        + p1 + "\";")

                    cursor.execute(
                        "update anime_girls set number_matches = number_matches + 1 where contender_name = \""
                        + p2 + "\";")

                    sql_command = f'''insert into rounds 
                                  (contender_A, contender_B, elo_A, elo_B, caipo, squid_cat, slifyre, radscorpion, 
                                   bake_it_jake, other)
                                   values( \"{p1}\", \"{p2}\", {data[p1][1]}, {data[p2][1]},
                                   \"{votes["Capio"]}\",  \"{votes["SquidCat"]}\",
                                   \"{votes["Slifyre"]}\",   \"{votes["Radscorpion"]}\",
                                   \"{votes["Lary"]}\", \"{votes["other"]}\" ); '''

                    cursor.execute(sql_command)

                    db.commit()

                    break

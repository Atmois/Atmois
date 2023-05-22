import random
import json
run = True # DO NOT CHANGE THIS MAKES EVERYTHING RUN
#_____________________________________________________________# Functions
#==================================# Add User to leaderboard
def addlb(name, score):
    with open('leaderboard.json', 'r+') as lb:
        data = json.load(lb)
        leaderboard = data['lb']
        #==================================# Checks if Username Exists
        for entry in leaderboard:
            if entry["name"] == name:
                if score > entry["score"]:
                    entry["score"] = score
                break
        #==================================# Adds score if it doesn't
        else:
            leaderboard.append({"name": name, "score": score})
        data['lb'] = leaderboard
        lb.seek(0)
        json.dump(data, lb, indent=2)
        lb.truncate()
        start()
#==================================# Load & Print Leaderboard
def loadll():
  with open('leaderboard.json') as lb:
    data = json.load(lb)
    print('Score | Name')
    for p in data['lb']:
      print(p['score'], '|', p['name']) 
#==================================# Sort Leaderboard
def sortll():
  with open('leaderboard.json', 'r+') as lb:
    data = json.load(lb)
    data['lb'] = sorted(data['lb'], key=lambda x: x['score'], reverse=True) # What actually sorts it
    lb.seek(0)  
    json.dump(data, lb, indent=2)
    lb.truncate()  
#==================================# Check if Username Exists
def usernamecheck(username):
    with open("logins.json", "r") as file:
        logins = json.load(file)
    for entry in logins:
        if entry["username"] == username:
            return True
    return False
#==================================# Login Check
def login(username, password):
    with open("logins.json", "r") as file:
        logins = json.load(file)
    for entry in logins:
        if entry["username"] == username and entry["password"] == password:
            return True
    return False
#==================================# Add new Login
def newuser():
    while run == True:
        try:
            #==================================# Asks for new Username
            with open("logins.json", "r") as file:
                logins = json.load(file)
            print("")
            username = input("New Username: ")
            #==================================# Checks if username already exists
            for entry in logins:
                if entry["username"] == username:
                    print("Username already exists.")
                    raise ValueError
            #==================================# Asks for new Password
            password = input("Password: ")
            #==================================# Saves new Login
            new_entry = {"username": username, "password": password}
            logins.append(new_entry)
            with open('logins.json', 'w') as file:
                json.dump(logins, file, indent=4)
            start() 
        #==================================# Error
        except ValueError:
            print("Try Again.")
            print("")
#_____________________________________________________________# Gamemode Selector
def start():
    #==================================# Vairables
    wordaddlist = []
    wordlist = []
    selectedwordlist = []
    entered_letters = []
    newword = "hello"
    lives = 6
    #==================================# Start of Code
    while run == True:    
        try:
            print("")
            mode = input("Please select if you would like play the game (Play), see the Leaderboard (LB), edit the list of words (Edit) or end the code (End): ") 
            mode = mode.lower() 
            #_____________________________________________________________# Editmode Selector
            if mode == "edit": 
                while run == True:
                    try:
                        print("")
                        editmode = input("Please select what you would like to edit, to add a entry (Add), to remove a entry (Remove) or to view the list (View): ") 
                        print("")
                        editmode = editmode.lower()
                    #_____________________________________________________________# Add word to database
                        if editmode == "add":
                            while run == True:
                                try:
                                    newword = input("Please enter a word that is less then 24 characters to be entered into the database: ")
                                    newword = newword.lower()
                                    newwordlencheck = len(newword)
                                    lettersonlycheck = newword.isalpha()
                                    #==================================# Dupelicate Check
                                    file = open("wordsto.txt", "r")
                                    data = file.read()
                                    wordlist = data.split("\n")
                                    file.close()
                                    if newword in wordlist:
                                        existingword = True
                                    else:
                                        existingword = False
                                    #==================================# Incorrect Entry Outputs
                                    if newwordlencheck > 24 or newwordlencheck < 1:
                                        print("Please enter a word less than 24 characters long or enter an word.")
                                        raise ValueError 
                                    elif lettersonlycheck == False:
                                        print("Please only enter characters.")   
                                        raise ValueError   
                                    elif existingword == True:
                                        print("This word already exists in the database.")
                                        existingword = False
                                        raise ValueError 
                                    else:
                                        wordaddlist.append(newword)
                                        with open('wordsto.txt', 'a') as file:
                                            for item in wordaddlist:
                                                file.write("\n" + item)
                                                file.close()
                                            print('Done')
                                            start()
                                except ValueError:
                                    print("Please try again.")
                                    print("")
                    #_____________________________________________________________# Remove word from database
                        elif editmode == "remove":
                            removeword = input("Please select a word to remove: ")
                            removeword = removeword.lower()
                    #==================================# Find word in database + find line number
                            with open('wordsto.txt', 'r') as file:
                                lines = file.readlines()

                            existingword = False
                            updated_lines = []

                            for line in lines:
                                if removeword not in line:
                                    updated_lines.append(line)
                                else:
                                    existingword = True

                            if existingword:
                                with open('wordsto.txt', 'w') as file:
                                    file.writelines(updated_lines)
                                print("The word", removeword, "has been removed from the database.")
                            else:
                                print("The word", removeword, "is not in the database.")

                            # No need to open the file here
                            start()

                    #_____________________________________________________________# View words in database
                        elif editmode == "view":
                            file = open("wordsto.txt", "r")
                            data = file.read()
                            wordlist = data.split("\n")
                            wordcount = len(wordlist)
                            print("There are", wordcount, "entries in the database.")
                            print(wordlist)
                            start()
                    #==================================# Wrong Input
                        else:
                            raise ValueError
                    except ValueError:
                        print("Please enter a valid Edit Mode.")
                        print("")
            #_____________________________________________________________# Play the game
            elif mode == "play":
            #==================================# Fetches and choses a random word and takes certain info from it
                print("")
                file = open("wordsto.txt", "r")
                data = file.read()
                wordlist = data.split("\n")
                file.close()
                selectedword = random.choice(wordlist)
                answer = "_" * len(selectedword) # Output
                print(selectedword)
                while run == True:
                    try:            
                        #==================================# Visual Life Counter
                        if lives == 1:
                            print("")
                            print("  +---+")
                            print("  |   |")
                            print("  O   |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("=======")
                            print("")
                        elif lives == 2:
                            print("")
                            print("  +---+")
                            print("  |   |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("=======")
                            print("")
                        elif lives == 3:
                            print("")
                            print("  +---+")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("=======")
                            print("")
                        elif lives == 4:
                            print("")
                            print("      +")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("      |")
                            print("=======")
                            print("")
                        elif lives == 5:
                            print("")
                            print("       ")
                            print("       ")
                            print("       ")
                            print("       ")
                            print("       ")
                            print("       ")
                            print("=======")
                            print("")                      
                        #==================================# Info
                        print("You have", lives, "lives!")
                        print("Letters you have guessed:", sorted(entered_letters))
                        print("Your current guess is:", answer)
                        #==================================# Enter Letter
                        letterchoice = input("Please input a letter in the English Alphabet to guess: ")
                        letterchoice = letterchoice.lower()
                        lettersonlyletterchoice = letterchoice.isalpha()
                        #==================================# Already Entered Letter
                        if letterchoice in entered_letters:
                            print("")
                            print("This letter has already been entered.")
                            raise ValueError          
                        elif lettersonlyletterchoice == False:
                            print("")
                            print("This is not a letter in the English Alphabet.")
                            raise ValueError
                        #==================================# More then 1 letter long 
                        if len(letterchoice) > 1:
                            print("")
                            print("Please enter a singular letter.")
                            raise ValueError          
                        #==================================# Check for the letter
                        elif any(ltr in letterchoice for ltr in selectedword):
                            entered_letters.append(letterchoice)
                            found = []
                            #==================================# Update answer variable
                            for x in range(0, len(selectedword)):
                                if selectedword[x] == letterchoice:
                                    found.append(x)
                                for x in range(0,len(found)):
                                    answer = list(answer)
                                    y = found[x]
                                    answer[y] = selectedword[y]
                                    answer = ''.join(answer)    
                        #==================================# Wrong Letter                  
                        else:
                            entered_letters.append(letterchoice)
                            lives = lives - 1
                            print("This letter is not in the word. You have lost a life.")
                        #==================================# Player Lose
                        if lives == 0:
                            print("")
                            print("Game over. The word was", selectedword)
                            print("")
                            print("  +---+")
                            print("  |   |")
                            print("  O   |")
                            print(" /|\  |")
                            print(" / \  |")
                            print("      |")
                            print("=======")
                            print("")                
                            start()
                        #==================================# Player Win
                        elif '_' not in answer:
                            print("")
                            print("You won.")
                            score = lives
                            addlb(username, int(score)) # Add player to leaderboard
                            start()      
                    #==================================# Error
                    except ValueError:
                        print("Please try again.")
                        print("")
            #_____________________________________________________________# View the leaderboard
            elif mode == "lb":
                print("")
                sortll()
                loadll()
                start()
            #==================================# End Code
            elif mode == "end":
                quit()
            #==================================# Wrong Input
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid mode.")
            print("")
#_____________________________________________________________# Login
print("")
accoption = input("Login (Login) or Create Account (Create): ")
accoption = accoption.lower()
#==================================# Login Mode
if accoption == "login":
    while run == True:
        try:
            print("")
            username = input("Enter your username: ")
            #==================================# Username Check
            if usernamecheck(username):
                password = input("Enter your password: ")
                #==================================# Password Check
                if login(username, password):
                    print("Login successful!")
                    start()
                #==================================# Invalid Password
                else:
                    print("")
                    print("Invalid password.")
                    raise ValueError
            #==================================# Invalid Username
            else:
                print("")
                print("Username not found.")
                raise ValueError
        #==================================# Error    
        except ValueError:
            print("Try Again.")
            print("")
#==================================# Create Account Mode
elif accoption == "create":
    newuser()
#==================================# Error
else:
    print("Invalid Option")
    quit()

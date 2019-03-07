# hangman.py
import random
from builtins import int, len, min, object

from ascii_file import HANGMANPICS
import re


class Hangman (object):
    """
    The hangman game.
    """
    def __init__(self, word='', lives=0):

        self.word = word
        self.guessed_letters = list()
        self.hidden_letters = list()
        self.attempt = 0
        self.lives = lives
        self.game_state = 1

    def ask_new_game(self):
        # ask for input whether the player wisher to play another game and reset certain variables if so.
        while True:
            game_state = input("Do you want to play again? (1 - for yes / 0 for no)")

            if game_state.isnumeric() == True:
                game_state = int(game_state)
                if game_state in [0, 1]:
                    if game_state == 1:
                        self.lives = 0
                        self.word = ''
                        self.guessed_letters = list()
                        self.hidden_letters = list()
                        self.attempt = 0
                        # print("You chose 1")
                        return
                    else:
                        # print("you chose 0")
                        self.game_state = 0
                        return
                else:
                    print("The value needs to be between 0 and 1")
                    continue
            else:
                print("The value needs to be between 0 and 1")
                continue

    def run_game(self):
        # initiate  a game session
        while True:
            if self.lives == 0:
                self.get_lives()
            if self.word == '':
                self.choose_word()
            if self.check_lives(self.lives) != 0:
                self.guess_letter()
                # print(self.game_state)
                self.ask_new_game()
                # print(self.game_state)
                if self.game_state == 0:
                    break
            else:
                self.get_lives()

    def display_letters(self):
        # returns an object to be displayed based on known and unkown letters in the word at play.
        self.hidden_letters = [x for x in self.word if
                          x not in self.guessed_letters]  # get all the letters that need to be hidden if they are not guessed
        if len(self.hidden_letters) != 0:
            # create a display text
            display_word = re.sub("[" + ''.join(self.hidden_letters ) + "]", "_", self.word)
        else:
            display_word = self.word
        return display_word

    def print_hangman(self):
        # prints the appropriate hangman pic based on the number of attmepts and lives.
        # choose pictures based on number of lines
        HANGMANPICS_NEW = HANGMANPICS[-int(self.lives):]

        print(HANGMANPICS_NEW[self.attempt-1])

    def guess_letter(self):
        # takes input from the player when guessing the letter, bassically the driver of the game.
        while True:

            dw = self.display_letters()
            if dw == self.word:

                print("The word was: \n" + dw)
                print("You won! Congrats!")

                break

            l = str(input(dw + "\nGuess a letter:"))
            if len(l) != 1:
                print("You input needs to be of length 1")
            else:
                if l.isalpha() == True:
                    if l in self.word:
                        if l in self.guessed_letters:  # choosing only the first letter
                            print("You already guessed that letter")
                            continue

                        else:
                            self.guessed_letters.append(l)
                            self.hidden_letters = [w for w in self.word if w not in self.guessed_letters]
                    else:

                        # print(HANGMANPICS_NEW[attempt])
                        self.attempt = self.attempt + 1
                        lives_left = self.lives - self.attempt

                        if self.attempt == self.lives:
                            self.print_hangman()
                            print("You dead.")
                            print("The word was " + self.word) # print the word
                            break
                        else:
                            self.print_hangman()
                            print("Wrong! You have %s lives left." % lives_left)
                else:
                    print("Your guess needs to be a letter")

    def check_lives(self, lives):
        if str(lives).isnumeric() == False:
            print("You need choose a numeric value, try again.")
            lives = 0

        else:
            if int(lives) not in [3, 4, 5, 6]:
                print("The number of lives needs to be between 3 and 6. Try again")
                lives = 0
            else:
                print("You chose %s lives" % lives)
        return int(lives)

    def get_lives(self, lives = 0):
        # this function asks the player to supply the number of lives in game
        number_of_lives = self.check_lives(lives)

        while int(number_of_lives) not in [3, 4, 5, 6]:
                number_of_lives = input('Enter the number of lives you wish to have between 3 and 6: ')
                number_of_lives = self.check_lives(number_of_lives)

        self.lives = number_of_lives

    def print_word(self):
        print("The word was: %" % self.word)

    def choose_word(self):
        # this function chooses a word to be played
        word_container = open("words.txt", "r")
        word_list = word_container.readlines()
        # trim end line
        clean_list = []

        for i in word_list:
            clean_list.append(i.replace("\n", ""))

        trimmed_list = list(filter(lambda i: len(i) > 3, clean_list))
        min_word_len = min([len(x) for x in trimmed_list])
        max_word_len = max([len(x) for x in trimmed_list])

        while True:
            word_len = input('Choose your difficulty, it needs between %s and %s' % (min_word_len, max_word_len))
            # print(word_len)
            if word_len.isnumeric() == False:
                print("You need choose a numeric value, try again.")
                continue
            else:
                word_len = int(word_len)
                if int(word_len) > max_word_len or int(word_len) < min_word_len:
                    print("The difficulty needs to be between %s and %s. Try again" % (min_word_len, max_word_len))
                    continue
                else:
                    print("You chose %s difficulty" % word_len)
                    # check if any words of such length exist
                    if len([x for x in trimmed_list if len(x) == word_len]) == 0:
                        print("Sorry, no words of such length exist. Try another value")
                        continue
                    else:
                        self.word = random.choice([x for x in trimmed_list if len(x) == word_len])
                        break


ccc = Hangman('zaidimas', 5)
# ccc.get_lives()
# ccc.choose_word()
# ccc.display_letters()
# ccc.guess_letter()
ccc.run_game()

# ccc.print_word()
# ccc.check_lives(9)
# ccc.get_lives(9)
2
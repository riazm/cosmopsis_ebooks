import sys;
import pdb;
import codecs;
import tkinter as tk
import time
from random import seed, choice, randrange
from string import ascii_letters

class markov_bot:
    table = {}
    startwords = []
    def generate_sentence(self):
        stopsentence = ('.', '!', '?',) # Cause a "new sentence" if found at the end of a word
    
        sentence = []
        entropy = 0
        (w1, w2) = choice(self.startwords)
    
        for i in (w1, w2):
            sentence.append(i)
    
        while len(" ".join(sentence)) < randrange(40, 130, 1):
            try:
                selection = self.table[(w1, w2)]
            except KeyError:
                break
            newword = choice(selection)
            entropy += len(selection)
            if newword in stopsentence:
                sentence[-1] = sentence[-1]+newword
            else:
                sentence.append(newword)
                w1, w2 = w2, newword
                print(entropy, sentence)
                
        return (" ".join(sentence), entropy/len(sentence))
    
    def generate_table(self, input):
        stopsentence = ('.', '!', '?',) # Cause a "new sentence" if found at the end of a word
        
    # GENERATE TABLE
        for statustext in input:
            w1, w2 = "\n", "\n"
            # build an array of sentence beginnings:
            try:
                self.startwords.append((statustext.split()[0], statustext.split()[1]))
            except IndexError:
                self.startwords.append((statustext, " "))
    
            for word in statustext.split():
                if w1.istitle():
                    self.startwords.append((w1,w2))
                if word[-1] in stopsentence:
                    self.table.setdefault( (w1, w2), [] ).append(word[0:-1])
                    w1, w2 = w2, word[0:-1]
                    word = word[-1]
                    
                self.table.setdefault( (w1, w2), [] ).append(word)
                w1, w2 = w2, word
        return True


source = sys.argv[1]

try:
    input = open(source, 'r')
except IOError:
    print("error, couldn't open the source text")

bot = markov_bot()
bot.generate_table(input)

seed(42)

colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
def do_stuff():
    entropy = 1 
    while entropy <= 1:
        tweet, entropy = bot.generate_sentence()

    s = tweet
    color = choice(colors)
    l.config(text=s, fg=color)
    root.after(750, do_stuff)

root = tk.Tk()
root.wm_overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.bind("<Button-1>", lambda evt: root.destroy())

l = tk.Label(text='', font=("Helvetica", 60))
l.pack(expand=True)

do_stuff()
root.mainloop()

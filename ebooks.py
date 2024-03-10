import sys;
import pdb;
import codecs;
import tkinter as tk
import time
import requests
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
                # if the last word ALREADY ended in a stop sentence, just return the sentence, don't bother trying to pad it with more punctuation
                if sentence[-1][-1] in stopsentence:
                    break
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
                self.startwords.append((statustext.split()[0],
                                        statustext.split()[1]))
            # sentence with less than 2 words
            except IndexError:
                pass
    
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

    def add_input(self,input):
        pass


def do_stuff():
    colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')    
    entropy = 1 
    # only update if we managed to get somethnig that's new
    while entropy <= 1:
        tweet, entropy = bot.generate_sentence()

    s = tweet
    color = choice(colors)
    l.config(text=s, fg=color)
    root.after(500, check_for_updates)
    root.after(750, do_stuff)

prev_prompts = 1
def check_for_updates():
    global prev_prompts
    prompts = int(requests.get("http://209.250.230.169:8000/myapp/prompt_count/").text)
    if prompts > prev_prompts:
        print("found " +str(prompts-prev_prompts)+ " new prompts, adding to bot")
        for prompt in range(prev_prompts, prompts+1):
            prompt_text = requests.get("http://209.250.230.169:8000/myapp/prompt/"+str(prompt)).text
            print(prompt_text, prompt)
            bot.add_input(prompt_text)
    prev_prompts = prompts 

source = sys.argv[1]

try:
    input = open(source, 'r')
except IOError:
    print("error, couldn't open the source text")

bot = markov_bot()
bot.generate_table(input)

seed(42)


root = tk.Tk()
root.wm_overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.bind("<Button-1>", lambda evt: root.destroy())

l = tk.Label(text='', font=("Oxygen", 60))
l.pack(expand=True)

do_stuff()
check_for_updates()
root.mainloop()

import random;
import sys;
import pdb;
import twitter;
import codecs;
import ConfigParser
        

def get_statuses(user):
    statuses = []
    api = twitter.Api()
    max_id = None
    total = 0
    while True:
        timeline = api.GetUserTimeline(user, count=75, max_id=max_id)
        newCount = ignCount = 0
        for s in timeline:
                statuses.append(s.text)
                newCount += 1
        total += newCount
        print "Fetched %d/%d new/total." % (
            newCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in timeline]) - 1
    
    statusfile = open('/home/r/Projects/ebooks/'+user, 'w')
    for i in statuses:
        statusfile.write(i.encode('utf-8')+'\n')
    statusfile.close()

    statuses = open('/home/r/Projects/ebooks/'+user, 'r')
    return statuses

def generate_sentence(table, startwords):
    stopsentence = ('.', '!', '?',) # Cause a "new sentence" if found at the end of a word

    sentence = []
    entropy = 0
    (w1, w2) = random.choice(startwords)

    for i in (w1, w2):
        sentence.append(i)

    while len(" ".join(sentence)) < random.randrange(40, 130, 1):
        try:
            selection = table[(w1, w2)]
        except KeyError:
            break
        newword = random.choice(selection)
        entropy += len(selection)
        if newword in stopsentence:
            sentence[-1] = sentence[-1]+newword
        else:
            sentence.append(newword)
        w1, w2 = w2, newword
    print entropy, len(sentence)
    return (" ".join(sentence), entropy/len(sentence))

def generate_table(input):
    stopsentence = ('.', '!', '?',) # Cause a "new sentence" if found at the end of a word
    
# GENERATE TABLE
    table = {}
    startwords = []
    
    for statustext in input:
        w1, w2 = "\n", "\n"
        # build an array of sentence beginnings:
        try:
            startwords.append((statustext.split()[0], statustext.split()[1]))
        except IndexError:
            startwords.append((statustext, " "))

        for word in statustext.split():
            if w1.istitle():
                startwords.append((w1,w2))
            if word[-1] in stopsentence:
                table.setdefault( (w1, w2), [] ).append(word[0:-1])
                w1, w2 = w2, word[0:-1]
                word = word[-1]
                
            table.setdefault( (w1, w2), [] ).append(word)
            w1, w2 = w2, word
    return (table, startwords)

def post_tweets(user, message):
    ebooks_cfg_parser = ConfigParser.ConfigParser()
    ebooks_cfg_parser.read('/home/r/Projects/ebooks/ebooks.cfg')
    user_key = ebooks_cfg_parser.get(user, 'access_token_key')
    user_secret = ebooks_cfg_parser.get(user, 'access_token_secret')

    api = twitter.Api(consumer_key='86eHOajQM074C9n5415Wfw', consumer_secret='uMQcE8oWXsWJHFVhBktLQlpqKuf6BQZtOdgY8B95wk', access_token_key=user_key, access_token_secret=user_secret)
    status = api.PostUpdate(message)
    print status.text
    return None

user = sys.argv[1]
entropy = 1 
try:
    input = open('/home/r/Projects/ebooks/'+user, 'r')
except IOError:
    input = get_statuses(user)

table, startwords = generate_table(input)

while entropy <= 1:
    tweet, entropy = generate_sentence(table, startwords)
post_tweets(user, tweet)


"""Typing test implementation"""

from re import L
from socket import EAI_BADHINTS
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1

    #paragraphs where all select func of the index values = true
    #return k index value of paragraphs
    n_para = []
    for curr_para in paragraphs:
        if select(curr_para):
            n_para += [curr_para]
    if k >= len(n_para):
        return ''
    else:
        return n_para[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2

    def match_word(topic, curr_para):
        for para_word in split(remove_punctuation(lower(curr_para))):
            if para_word in topic:
                return True
        else: 
            return False
    return lambda curr_para: match_word(topic, curr_para)
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    
    #go through each word in typed words and the corresponding word in source words
    match = 0
    index = 0
    while index < len(source_words) and index < len(typed_words):
        typed_word = typed_words[index]
        source_word = source_words[index]
        if typed_word == source_word:
            match += 1
        index += 1
    if len(source_words) == 0 and len(typed_words) == 0:
        return 100.0
    elif len(typed_words) == 0 or len(source_words) == 0:
        return 0.0
    else:
        return (match / len(typed_words)) * 100

    #match goes up by one if they match/are the same

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    
    typed_char = len(typed)
    elapsed_min = 60 / elapsed
    return (typed_char / 5) * elapsed_min


    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    auto_words = []
    diff_i = []
    corr_i = 0
    min_diff = limit
    for word in word_list:
        if typed_word == word:
            return typed_word
        diff = diff_function(typed_word, word, limit)
        if diff <= limit:
            auto_words += [word]
            diff_i += [diff]
    if len(auto_words) > 0:
        for i in range(len(diff_i)):
            if diff_i[i] < min_diff:
                min_diff = diff_i[i]
                corr_i = i
        return auto_words[corr_i]
    else:
        return typed_word

    # END PROBLEM 5


def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    def word(typed, source, i, edits, limit):
        if i < len(source):
            if typed[i] == source[i]:
                i += 1
                return word(typed, source, i, edits, limit)
            else:
                edits += 1
                i += 1
                if edits > limit:
                    return edits
                else:
                    return word(typed, source, i, edits, limit)
        else:
           return edits

    if len(typed) == len(source):
        return word(typed, source, 0, 0, limit)
    elif len(typed) < len(source):
        return word(typed, source[:len(typed)], 0, 0, limit) + (len(source)-len(typed))
    else:
        return word(typed[:len(source)], source, 0, 0, limit) + (len(typed)-len(source))
    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.
    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    def sub(start, goal, limit):
        return 1 + minimum_mewtations(start[1:], goal[1:], limit - 1)

    def add(start, goal, limit):    
        return 1 + minimum_mewtations(start, goal[1:], limit - 1)

    def remove(start, goal, limit):
        return 1 + minimum_mewtations(start[1:], goal, limit - 1)


    if start == goal:
        return 0 
    elif limit < 0:
        return 1
    elif len(start) == 0:
        return len(goal)
    elif len(goal) == 0:
        return len(start)
    elif start[0] == goal[0]:
            return minimum_mewtations(start[1:], goal[1:], limit)
    else:
        edit_add = add(start, goal, limit)
        edit_sub = sub(start, goal, limit)
        edit_remove = remove(start, goal, limit)
        return min(edit_add, edit_sub, edit_remove)

    

def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    
    def progress(typed, prompt, i):
        if i < len(typed) and typed[i] == prompt[i]:
            i +=1 
        else:
            progress_ratio = i / len(prompt)
            upload({'id': user_id, 'progress' : progress_ratio})
            return progress_ratio
        return progress(typed, prompt, i)
    
    return progress(typed, prompt, 0)

    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    def player_times (times_per_player, i, time_i, times_list_i, times_list):
        if i < len(times_per_player):
            if time_i < len(times_per_player[i]) - 1:
                times_list[times_list_i] += [abs(times_per_player[i][time_i] -times_per_player[i][time_i + 1])]
                time_i += 1
            else:
                i += 1
                time_i = 0
                times_list_i += 1
        else:
            return times_list
        
        return player_times(times_per_player, i, time_i, times_list_i, times_list)
    
    times_list = []
    times_list_i = 0
    while times_list_i < len(times_per_player):
        times_list.append([])
        times_list_i += 1
    
    return match(words, player_times(times_per_player, 0, 0, 0, times_list))

    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    
    


    def make_list(i, players, words_list):
        times_list = []
        if i < len(word_indices):
            word = get_word(match, i)
            while players < len(player_indices):
                player_time = time(match, players, i)
                times_list += [player_time]
                players += 1
            words_list[(times_list.index(min(times_list)))] += [word]
            i += 1
        else:
            return words_list
        return make_list(i, 0, words_list)

    words_list = []
    words_list_i = 0
    while words_list_i < len(player_indices):
        words_list.append([])
        words_list_i += 1

    return make_list(0 , 0, words_list)

    # END PROBLEM 10


def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(match["words"]), "word_index out of range of words"
    return match["words"][word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match["words"]), "word_index out of range of words"
    assert player_num < len(match["times"]), "player_num out of range of players"
    return match["times"][player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match dictionary and returns a string representation of it"""
    return f"match({match['words']}, {match['times']})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)

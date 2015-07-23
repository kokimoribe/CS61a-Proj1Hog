"""The Game of Hog"""

from dice import four_sided_dice, six_sided_dice, make_test_dice
from ucb import main, trace, log_current_line, interact

goal = 100          # The goal of Hog is to score 100 points.
commentary = True  # Whether to display commentary for every roll.
MAX_NUM_ROLLS = 10

def roll_dice(num_rolls, dice=six_sided_dice, who='Boss Hogg', ones_lose=True):
    """Calculate WHO's turn score after rolling DICE for NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A function of no args and returns an integer outcome.
    who:        Name of the current player, for commentary.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    assert num_rolls <= 10, 'Number of dice must not exceed 10.'

    score = 0
    pigOut = False

    for i in range(num_rolls):

        roll = dice()
        if commentary:
            announce(roll, who)
        if roll == 1 and ones_lose:
            pigOut = True
        else:
            score += roll

    if pigOut:
        if commentary:
            print(who + " rolled a 1 and pigs out!")
        score = 1

    return score

def take_turn(num_rolls, opp_score, dice = six_sided_dice, who = 'Boss Hogg', ones_lose=True):
    """Simulate a turn in which WHO chooses to roll NUM_ROLLS, perhaps 0.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args and returns an integer outcome.
    who:             Name of the current player, for commentary.
    """

    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'

    if commentary:
        print(who, 'is going to roll', num_rolls, 'dice')

    score = 0
    if num_rolls == 0:
        score = 1 + opp_score//10
    else:
        score = roll_dice(num_rolls, dice, who, ones_lose)

    if score % 6 == 0:
        if commentary:
            print("Touchdown! {0}'s score is a multiple of 6. +{1} extra points!".format(who, score//6))
        score += score//6

    if commentary:
        print(who + " scored " + str(score) + " points this turn.")
    return score

def take_turn_test():
    """Test the roll_dice and take_turn functions using test dice."""
    print('-- Testing roll_dice with deterministic test dice --')
    dice = make_test_dice(4, 6, 1)
    assert roll_dice(2, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert roll_dice(3, dice) == 1, 'Third roll is a 1'

    dice = make_test_dice(1, 2, 3)
    assert roll_dice(3, dice) == 1, 'First roll is a 1'

    print('-- Testing take_turn --')
    dice = make_test_dice(4, 6, 1)
    assert take_turn(2, 0, dice) == 10, 'First two rolls total 10'

    dice = make_test_dice(4, 6, 1)
    assert take_turn(3, 20, dice) == 1, 'Third roll is a 1'

    print('-- Testing Free Bacon rule --')
    assert take_turn(0, 34) == 4, 'Opponent score 10s digit is 3'
    assert take_turn(0, 71) == 8, 'Opponent score 10s digit is 7'
    assert take_turn(0,  7) == 1, 'Opponont score 10s digit is 0'

    print('-- Testing Touchdown rule --')
    dice = make_test_dice(6)
    assert take_turn(1, 0, dice) == 7, 'Original score was 6'
    assert take_turn(2, 0, dice) == 14, 'Original score was 12'
    assert take_turn(0, 50, dice) == 7, 'Original score was 6'

    print('-- Testing 49ers rule --')
    dice = make_test_dice(1)
    assert roll_dice(3, dice, ones_lose=False) == 3, '49ers rule in effect'
    assert take_turn(10, 0, dice, ones_lose=False) == 10, '49ers rule in effect'
    assert take_turn(6, 0, dice, ones_lose=False) == 7, '49ers and Touchdown rule'

    '*** You may add more tests here if you wish ***'

    print('Tests for roll_dice and take_turn passed.')


# Commentator

def announce(outcome, who):
    """Print a description of WHO rolling OUTCOME."""
    print(who, 'rolled a', outcome)
    print(draw_number(outcome))

def draw_number(n, dot='*'):
    """Return a text representation of rolling the number N.
    If a number has multiple possible representations (such as 2 and 3), any
    valid representation is acceptable.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------

    >>> print(draw_number(6, '$'))
     -------
    | $   $ |
    | $   $ |
    | $   $ |
     -------
    """
    """
    1 = c
    2 = b or f
    3 = (b or f) and c
    4 = b and f
    5 = b and f and c
    6 = b and s and f
    """
    #draw_dice function can only draw a max of 7 dots.
    #Can you use "and" operator?
    assert type(n)==int
    assert n <= 7
    assert n > 0

    c = f = b = s = False

    #switch statement?
    #how to randomly choose orientation of 2 and 3?
    
    if n == 1:
        c = True
    elif n == 2:
        b = True
    elif n == 3:
        b,c = True, True
    elif n == 4:
        b,f = True, True
    elif n == 5:
        b,c,f = True, True, True
    elif n == 6:
        b,f,s = True, True, True
    elif n == 7:
        b,c,f,s = True, True, True, True
    
    return draw_dice(c,f,b,s,dot)

def draw_dice(c, f, b, s, dot):
    """Return an ASCII art representation of a die roll.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.

     -------
    | b   f |
    | s c s |
    | f   b |
     -------

    The sides with 2 and 3 dots have 2 possible depictions due to rotation.
    Either representation is acceptable.

    This function uses Python syntax not yet covered in the course.

    c, f, b, s -- booleans; whether to place dots in corresponding positions.
    dot        -- A length-one string to use for a dot.
    """
    assert len(dot) == 1, 'Dot must be a single symbol'
    border = ' -------'
    def draw(b):
        return dot if b else ' '
    c, f, b, s = map(draw, [c, f, b, s])
    top = ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c, s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

def num_allowed_dice(score, opponent_score):
    """Return the maximum number of dice allowed this turn. The maximum
    number of dice allowed is 10 unless the sum of SCORE and
    OPPONENT_SCORE has a 7 as its ones digit.

    >>> num_allowed_dice(1, 0)
    10
    >>> num_allowed_dice(5, 7)
    10
    >>> num_allowed_dice(7, 10)
    1
    >>> num_allowed_dice(3, 24)
    1
    """

    if (score + opponent_score)%10 == 7:
        return 1

    return 10

def select_dice(score, opponent_score):
    """Select 6-sided dice unless the sum of scores is a multiple of 7.

    >>> select_dice(4, 24) == four_sided_dice
    True
    >>> select_dice(16, 64) == six_sided_dice
    True
    """
    if (score + opponent_score) % 7 == 0:
        return four_sided_dice

    return six_sided_dice

def other(who):
    """Return the other player, for players numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2

def name(who):
    """Return the name of player WHO, for player numbered 0 or 1."""
    if who == 0:
        return 'Player 0'
    elif who == 1:
        return 'Player 1'
    else:
        return 'An unknown player'

def play(strategy0, strategy1):

    """Simulate a game and return 0 if the first player wins and 1 otherwise.

    A strategy function takes two scores for the current and opposing players.
    It returns the number of dice that the current player will roll this turn.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    strategy0:  The strategy function for player 0, who plays first.
    strategy1:  The strategy function for player 1, who plays second.
    """

    who = 1 # Which player is about to take a turn, 0 (first) or 1 (second)
    p0 = 0
    p1 = 0
    turn_number = 0

    while p0 < goal and p1 < goal:
        who = other(who)
        max_dice = num_allowed_dice(p0,p1)

        if who == 0:
            num_rolls = strategy0(p0,p1)

            if num_rolls > max_dice:
                num_rolls = max_dice

            p0 += take_turn(num_rolls, p1, select_dice(p0, p1), name(who), (p0 != 49))

        else:            
            num_rolls = strategy1(p1, p0)

            if num_rolls > max_dice:
                num_rolls = max_dice

            p1 += take_turn(num_rolls, p0, select_dice(p1, p0), name(who), (p1 != 49))

    return who

# Basic Strategy

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two game scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice to roll.

    If a strategy returns more than the maximum allowed dice for a turn, then
    the maximum allowed is rolled instead.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


# Experiments (Phase 2)

def make_average(fn, num_samples=100):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> avg_dice = make_average(dice)
    >>> avg_dice()
    3.75
    >>> avg_score = make_average(roll_dice)
    >>> avg_score(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """

    def averageFN(*args):
        total = 0
        for i in range(num_samples):
            total += fn(*args)
        return total/num_samples

    return averageFN

def compare_strategies(strategy, baseline=always_roll(5)):
    """Return the average win rate (out of 1) of STRATEGY against BASELINE."""
    as_first = 1 - make_average(play)(strategy, baseline)
    as_second = make_average(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for MAKE_STRATEGY to use against
    the always-roll-5 baseline, between LOWER_BOUND and UPPER_BOUND (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range.
    upper_bound -- upper bound of the evaluation range.
    """
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print('Win rate against the baseline using', value, 'value:', win_rate)
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_experiments():
    """Run a series of strategy experiments and report results."""
    result = eval_strategy_range(always_roll, 1, 10)
    print('Best always_roll strategy:', result)

    if True: # Change to True when ready to test make_comeback_strategy
        result = eval_strategy_range(make_comeback_strategy, 5, 15)
        print('Best comeback strategy:', result)

    if True: # Change to True when ready to test make_mean_strategy
        result = eval_strategy_range(make_mean_strategy, 1, 10)
        print('Best mean strategy:', result)

    return result

    "*** You may add additional experiments here if you wish ***"


# Strategies

def make_comeback_strategy(margin, num_rolls=5):
    """Return a strategy that rolls one extra time when losing by MARGIN."""
    
    def strategy(score, opponent_score):

        if (opponent_score - score) >= margin:

            return num_rolls + 1

        return num_rolls

    return strategy

def make_mean_strategy(min_points, num_rolls=5):
    """Return a strategy that attempts to give the opponent problems."""
    
    def strategy(score, opponent_score):

        turn_score = 1 + opponent_score // 10
        if turn_score % 6 == 0:
            turn_score += turn_score // 6

        if turn_score >= min_points:

            score_sum = score + opponent_score + turn_score

            #multiples of 7 are more likely than a score ending in 7 (i think) so check multiple 7 first
            #score_sum will always be greater than 0
            if (score_sum % 7) == 0 or (score_sum % 10) == 7:
                return 0
        return num_rolls

    return strategy

def final_strategy(score, opponent_score):
    """
    If score is 49, roll max dice.

    If using Free Bacon is advantageous, roll 0 dice.
        Free Bacon will be advantageous when:
            -It gives you enough points to win.
            -It gives you a score of 49.
            -The opponent will be Hog Tied and/or Hog Wild after.
            -It gives you more points than the expected value if you are Hog Tied and/or Hog Wild.

    If current sum results in Hog Wild, roll 4 dice.
    
    If using max dice is needed, roll 10 dice.
        Rolling max dice is needed when:
            -You are very behind and opponent will likely win on the next turn.
            -Pigging out results in a score of 49.

    Else, roll whatever number dice the comeback strategy returns.

    """
    difference = opponent_score - score
    current_sum = score + opponent_score

    """Functions specific to strategy are defined here, the actual strategy is shown after"""

    def isHogTied(total_score = current_sum):

        return (total_score % 10) == 7

    def isHogWild(total_score = current_sum):

        return (total_score != 0) and (total_score % 7) == 0

    def is49ers(input_score = score):

        return input_score == 49

    def calculateFreeBacon(x):

        freeBacon = (1 + (x // 10))
        
        if freeBacon % 6 == 0:
            freeBacon += freeBacon // 6

        return freeBacon

    def useFreeBacon():
        #continuous if statements vs if elif?
        future_score = score + freeBacon

        if (future_score >= goal):

            #print("using Free Bacon because you win on this turn")
            return True


        future_sum = future_score + opponent_score

        #don't use free bacon if opponent is very close to winning
        if (goal - opponent_score) >= 5:

            if (is49ers(future_score)):

                #print("using Free Bacon because you get 49")
                return True

            if isHogTied(future_sum) or isHogWild(future_sum):

                    return True

            if hogTied or hogWild:

                if hogTied and hogWild:
                    #Expected score using one four_sided_dice = 2.5
                    #use freeBacon if the points return greater than average score
                    if freeBacon >= 3:
                        return True

                if hogTied:
                    #Expected score using one six_sided_dice = 3.7
                    if freeBacon >= 4:
                        return True

                if hogWild:
                    #Expected score with four_sided_dice using number of dice that gives highest expected score = 4.6
                    if freeBacon >= 5:
                        return True

        return False

    def rollMaxOrOne():
        """This will return true if opponent will likely win the next turn and you are very behind
        OR if pigging out on your turn results in a 49er"""

        return (((goal - opponent_score) <= 10 and difference >= 42) or score == 48)

    def expectedValue(n, m):
        """returns the expected(averaged) score in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0 

    def chanceOfExact(x,n,m):
        """returns the chance of getting an exact score of x in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0

    def chanceOfGettingGreater(x,n,m):
        """returns the chance of getting a score of x OR greater in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0

    def maxScore(n,m):
        """returns the maximum score a player can get in one turn using n number of dice each with m number of sides"""
        return 0

    freeBacon = calculateFreeBacon(opponent_score)
    hogTied = isHogTied()
    hogWild = isHogWild()

    if (is49ers()):

        #print("Gonna roll 10 because 49ers")
        #return 10
        return 49

    if (useFreeBacon()):

        #print("Gonna roll 0 because Free Bacon")
        return 0

    if (hogWild):

        #print("Gonna roll 4 because hog wild")
        return 4

    if(rollMaxOrOne()):

        #print("Gonna roll 10 because max or one")
        return 10

    strat = make_comeback_strategy(10)

    if (strat(score,opponent_score) != 5):

        #print("Gonna roll 6 because comeback time")
        return 6

    #print("Just gonna go with normal 5")
    return 5

def final_strategy_ver2(score, opponent_score):
    """
    find default strategy roll
    see if roll gives opponent advantage
    if opponent gets advantage, reroll to a 5

    """
    difference = opponent_score - score
    current_sum = score + opponent_score

    """Functions specific to strategy are defined here, the actual strategy is shown after"""

    def isHogTied(total_score = current_sum):

        return (total_score % 10) == 7

    def isHogWild(total_score = current_sum):

        return (total_score != 0) and (total_score % 7) == 0

    def is49ers(input_score = score):

        return input_score == 49

    def calculateFreeBacon(x):

        freeBacon = (1 + (x // 10))
        
        if freeBacon % 6 == 0:
            freeBacon += freeBacon // 6

        return freeBacon

    def useFreeBacon():
        #continuous if statements vs if elif?
        future_score = score + freeBacon

        if (future_score >= goal):

            #print("using Free Bacon because you win on this turn")
            return True


        future_sum = future_score + opponent_score

        #don't use free bacon if opponent is very close to winning
        if (goal - opponent_score) >= 5:

            if (is49ers(future_score)):

                #print("using Free Bacon because you get 49")
                return True

            if isHogTied(future_sum) or isHogWild(future_sum):

                    return True

            if hogTied or hogWild:

                if hogTied and hogWild:
                    #Expected score using one four_sided_dice = 2.5
                    #use freeBacon if the points return greater than average score
                    if freeBacon >= 3:
                        return True

                if hogTied:
                    #Expected score using one six_sided_dice = 3.7
                    if freeBacon >= 4:
                        return True

                if hogWild:
                    #Expected score with four_sided_dice using number of dice that gives highest expected score = 4.6
                    if freeBacon >= 5:
                        return True

        return False

    def rollMaxOrOne():
        """This will return true if opponent will likely win the next turn and you are very behind
        OR if pigging out on your turn results in a 49er"""

        return (((goal - opponent_score) <= 10 and difference >= 42) or score == 48)

    def expectedValue(n, m):
        """returns the expected(averaged) score in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0 

    def chanceOfExact(x,n,m):
        """returns the chance of getting an exact score of x in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0

    def chanceOfGettingGreater(x,n,m):
        """returns the chance of getting a score of x OR greater in one turn given n number of dice each with m number of sides"""
        """return value also takes into account of the pig out rule and touchdown rule"""
        return 0

    def maxScore(n,m):
        """returns the maximum score a player can get in one turn using n number of dice each with m number of sides"""
        return 0

    freeBacon = calculateFreeBacon(opponent_score)
    hogTied = isHogTied()
    hogWild = isHogWild()

    def doubleCheck(n):

        if n == 0:

            futureScore = score + freeBacon
            opponent_roll = final_strategy(opponent_score, future_score)

            #if opponent_roll ==
        return 0

    return 0



def final_strategy_test():
    """Compares final strategy to the baseline strategy."""
    print('-- Testing final_strategy --')
    print('Win rate:', compare_strategies(final_strategy))



# Interaction.  You don't need to read this section of the program.

def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive tactic.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    print('Current score:', score, 'to', opponent_score)
    while True:
        response = input('How many dice will you roll? ')
        try:
            result = int(response)
        except ValueError:
            print('Please enter a positive number')
            continue
        if result < 0:
            print('Please enter a non-negative number')

        if result > MAX_NUM_ROLLS:
            print('Please enter a number that does not exceed {0}'.format(MAX_NUM_ROLLS))
        else:
            return result

def play_interactively():
    """Play one interactive game."""
    global commentary
    commentary = True
    print("Shall we play a game?")
    winner = play(interactive_strategy, always_roll(5))
    if winner == 0:
        print("You win!")
    else:
        print("The computer won.")

def play_basic():
    """Play one game in which two basic strategies compete."""
    global commentary
    commentary = True
    winner = play(always_roll(5), always_roll(6))
    if winner == 0:
        print("Player 0, who always wants to roll 5, won.")
    else:
        print("Player 1, who always wants to roll 6, won.")

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--take_turn_test', '-t', action='store_true')
    parser.add_argument('--play_interactively', '-p', action='store_true')
    parser.add_argument('--play_basic', '-b', action='store_true')
    parser.add_argument('--run_experiments', '-r', action='store_true')
    parser.add_argument('--final_strategy_test', '-f', action='store_true')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if execute:
            globals()[name]()


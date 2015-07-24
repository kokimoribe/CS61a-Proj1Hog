###About this project:

- **Project date**: 1/27/2013

- **Objective**: To develop a simulator and multiple strategies for the dice game Hog.

- **Outcome**: Successfully developed a working simulator and several strategies for the dice game Hog in Python. The final strategy that was developed maintained a 64.2% win rate against the baseline strategy after testing many runs through the simulator.
	
- **Contribution**: Implemented higher-order functions, experimented with random number generators, and generated ASCII art to represent dice outcomes in the simulator. Carefully planned out algorithms for implementing the simulator and the game’s strategies and revised code for organization and efficiency.


###How to use:

1. Learn the rules of Hog [hog_rules.txt](hog_rules.txt)
2. 
      - To simulate a single game in which player 0 always wants to roll 5 dice, while player 1 always wants to roll 6 dice, enter the following line into your terminal: ```python3 hog.py -b```
     
     
      - To play an interactive game of Hog against an opponent that always wants to roll 5 dice, enter the following line into your terminal: ```python3 hog.py -p```
      
      - To run a series of strategy experiments, which play many games of Hog and print the average results, enter the following line into your terminal: ```python3 hog.py -r```
      
      - To test the implemented final strategy against the baseline strategy, enter the following line into your terminal: ```python3 hog.py -f```

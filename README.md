## PART 1: RAICHU
To find the best possible move for a given player with the given current board state.

#### Search Abstraction:
##### Initial State: 
Given a board of size n*n with three different pieces(Pichu,Pikachu,Raichu) of two different colors(white and black).

##### Terminal State: 
Goal state is defined when all the pieces of opposite player are killed(the count of all the pieces of same color for a particular player is 0).

##### Successors: 
The successor function generates new boards for all the possible moves of each given piece in the board. 

-> Possible moves for Pichu:
* All the positions where pichu can move forward diagonally given that the square is empty.
* All the positions where it can jump over a single pichu of opposite color by moving 2 squares forward diagonally given that the square is empty. The jumped piece would then be removed from the board.

-> Possible moves for Pikachu:
* ALl the positions where it can move either forward left,right or right but not diagonally given that the all the squares in between are empty.
* All the positions where it can jump over a single Pichu/Pikachu of opposite color by moving 2 or 3 squares forward diagonally given that all of the squares between Pikachu's starting position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece would then be removed from the board.
	   
-> Possible moves for Raichu(created when a Pichu or Pikachu reaches opposite end of the board):
* Returns moves of all positions where it can jump forward/backward right,left or diagonally.
* Returns all positions where it can jump over a single Pichu/Pikachu/Raichu of opposite color and landing any number of squares forward/backward left,right or diagonally given that the squares between Raichu's start position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece would then be removed from the board.



##### Evaluation function: 

* Weighted difference between White pokemons and black pokemons:
 
10 *(count(white pichus) - count(black pichus)) + 15 * (count(white pikachus) - count(black pikachus)) + 50 * (count(white raichus)-count(black raichus))

where,
	10 is the weight we are assigning to pichus
	15 is the weight assigned to pikachus
	50 is the weight assigned to raichus
	
Multiplier - 1 if player is white and -1 if player is black

* Also, as part of generating our successors for Pichus and Pikachus- we added the cumulative heights of the board for these pieces so as to make them go vertically ahead on the board and become Raichu.

##### Solution Overview:

We have solved this problem by implementing minimax algorithm. To further optimize the computation time, we have used Alpha-Beta pruning technique because this allows us to search much faster and traverse to deeper levels of the game tree. It cuts off the branches in the game tree which need not be explored as there is a much better move available.

###### Parameters:
	* Alpha - gives the best value of the maximizer at the current level
	* Beta - gives the best value of the minimizer at the current level

We have initialised default values for Alpha and Beta as -10000000,10000000 respectively. 

These functions below calculate the Alpha and Beta values and back these upwards to the game tree:
* def maxvalue(successor, alpha_val, beta_val, depth_level, player, depth_limit, N,timelimit): returns best move for the max player.
* def minvalue(successor: Board, alpha_val, beta_val, depth_level, player, depth_limit, N,timelimit): returns best move for the opponent player.


##### Difficulties faced:

* The code execution was stopping after a specific time-limit without reaching the terminal state. In this case, we worked on our algorithm for the evaluation function in order to give an incentive for the piece to move in the vertical direction.


## PART 2: THE GAME OF QUINTRIS
To find highest possible score in the game by arranging the pieces in the best way posisble.

#### Search Abstraction:
##### Initial State: 
Given a blank board of 25 rows and 15 columns with no pieces as yet.

##### Terminal State: 
It is defined when the board fills up completely.
Player loses when a row of new pieces cannot be added to the board.

Goal is to get the highest possible score at this state.

##### Successors: 
To find all successive moves we created:
* Piece Successors- generates new pieces after rotations (90 degree, 180 degree, 270 degree) and flip (horizontal flip) for all the defined pieces.
In the program, rt -> all possible rotations and hrt -> hortizontal flips and all possible rotations 
* Board Successors- traverses through each column in the board and check if at all the placement of any piece successor would be colliding with anything beneath it, and then goes on to place it on the board. Returns all the possible boards when the condition above is satisfied.

##### Evaluation function: 
Parameters considered for the heuristic:

Awards:
* for clearing a row
* for touching the base of the board
* for touching the edges of the board

Costs- Penalize if:
* cumulative height of all columns rises
* there are holes being formed in the board - empty spaces in rows
* there are pits being formed in the board - empty columns
* there is bumpiness on the board - uneven heights of all columns

#### Solution Overview:
* Generates successor for each piece and finds the best possible position to place it on the board using heuristic

We were working on implementing Expectiminimax to get to the best possible placement of the pieces on the board, although we were not able to do so successfully and hence opted to go ahead with a double greedy solution to our problem.


##### Difficulties faced:
* We found that assigning weights for each parameter in our heuristic was the most challenging part of the problem. After trying many permutations and combinations we decided to go ahead with certain values for considered parameters.
* Implementing Expectiminimax- had certain issues in getting values for probability predictions

## PART 3:  TRUTH BE TOLD
Create a classification model, train it using the training data, and  predict the class for the object of words.

#### Search Abstraction:

Having used Naive Bayes theorm to find the likelihood of  an object belonging to a particular class, which states that: 
	P(Posterior) prob i.e. P(Class | object of words ) = P(Likelihood) prob * P(Prior) 
Prob where the Prior prob of each class is equal to the ratio of the number of objects present in that particular category to the total num of objects in the data set and likelihood probability of a word given category is the number of repetitions of that particular word in that category to the total number of words in that category. This was done with the help of "word_of_bags" generated from the training data.

##### Initial State: 
The initial state is where the classifier is yet to be fed with the training data to learn and understand the probabilities

##### Terminal State: 
Being able to classify the given test data more accurately.

##### Evaluation function: 
The item will be allocated to the class/category that receives the highest P(Posterior) probability value.

Because the denominator (prior prob of each class) of the Bayes law will be constant for all classes in the current data set, we shall ignore it here.

So all we're doing is maximizing the numerator for all the tweets and then picking the best one.

P(w1,w2,w3,.....) = P(w1) * P(w2) * P(w3) * P(w4) * P(w5) * P(w6) * P(w7) * P(w8) * P(w9) * P(w10) * P(w11) * P(w12) * P(w13) * P(w14

The special characters are removed from the training data so as to avoid the overfitting of the model.

While the accuracy for the GIVEN test data can be improved by using the overfitted model, it falls short of being able to be a generic-good classifier.

##### Challenges 

Tackling the new words from the test-data was essential. While we have tried to find`text similarity` between the new word and the existing bag of words by using techniques like jaro-winkler similarity and jaro-similarity, the complexity skyrocketted, and was unable to continue in any reasonable amount of time. Also, laplace smoothening was attempted but there were no improvements to the accuray as a whole.

While the accuracy was at `85%` when the special charecters were not eliminated, this we've found was an overfitting of the model, especially because, the probabilities would be much higher for such exact matches and can thus guide the classifier for a better and higher accuracy. However, this is not as "generic" as a classifier can get. 

Hence, keeping the best principles and practices in mind, we have settled for a trade-off between the generalization and specification.































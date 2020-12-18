<a id='section_6'></a>

<img src="https://cdn.hipwallpaper.com/i/66/61/cb1GgL.jpg" width="1000">

<h1 align = "center">NFL-Big-Data-Bowl-2021</h1>

<p align = "center"><img src="https://user-images.githubusercontent.com/62911364/102659702-7e248600-413f-11eb-8d68-7f6a003924a0.png"></p>
<h2 align = "center">Authors: Austin Aranda, George Arredondo, Angel Gomez, Gilbert Noriega</h2>

[About the Project](#section_1) || [Data Dictionary](#section_2) ||  [Initial Hypotheses](#section_3) || [Project Plan](#section_4) || [How to Reproduce](#section_5)

<br>

<a id='section_1'></a>
## About the Project: 
> Football is a physical sport that requires true teamwork to win a game. Offense usually gets all the glitz and glamour of scoring while defenses often don't get the credit they deserve. Our Data Science Team ```Fourth and Four``` will dive through the A gap to understand what can help defenses stop a completed pass. We will be using the [NFL Big Data Bowl 2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021/overview) data sets to use existing features and engineer features to create a classification machine learning model that will accurately predict a defense stopping a completed pass.
___

<br>

>*Acknowledgement:The dataset was provided by kaggle.com, originally sourced by nextgenstats.nfl.com* 

___

<br>

<p align = "center">
<img src="https://user-images.githubusercontent.com/62911364/102655731-6bf31980-4138-11eb-9b16-0a5c5aa93b27.gif">
</p>

## Goals
Our goal for this project is to use different classification models to accurately predict a defense stopping a completed pass during the NFL 2018 regular season. We will deliver the following in a github repository: 
>
> - A clearly named final notebook. This notebook will contain markdown documentation of what we are doing and the code to accomplish the task.
> - A README.md that thoroughly explains our project, how to reproduce the work done, and details along the way to help answer what defenses can do to stop a completed pass. 
> - Python modules that automate the data acquisition, preparation and modeling processes. These modules will be imported and used in the final notebook.

[back to the top](#section_6)

___

<br>

<a id='section_2'></a>
## Data Dictionary

<details>
  <summary>Dictionary</summary>

| **Feature** | **Definition** |
| --- | --- |
| time | Time stamp of play (time, yyyy-mm-dd, hh:mm:ss) |
| x | Player position along the long axis of the field (x), 0 - 120 yards. See Figure 1 below. (numeric) |
| y | Player position along the short axis of the field (y), 0 - 53.3 yards. See Figure 1 below. (numeric) |
| s | Speed in yards/second (numeric) |
| a | Acceleration in yards/second^2 (numeric) |
| dis | Distance traveled from prior time point, in yards (numeric) |
| o |  Player orientation (deg), 0 - 360 degrees. See Figure 1 below (numeric)
| nflId | Player identification number, unique across players (numeric) |
| displayName | Player name (text) |
| jerseyNumber | Jersey number of player (numeric) |
| position | Player position group i.e. QB, RB, WR, LB, CB (text) |
| frameId | Frame identifier for each play, starting at 1 (numeric) |
| gameId | Unique game identifier (numeric)
| playId | Play identifier that is not unique across games (numeric)
| playDirection | Direction that the offense is moving (text, left or right)
| route | Route ran by offensive player (text) |
| week | Week of game 1-18 (numeric) |
| height | Height of player in inches (numeric) |
| weight | Weight of player in lbs (numeric) |
| birthDate | Birthdate of player YYYY-MM-DD (text) |
| collegeName | Name of College player attended (text) |
| age | Age of player (text) |
| time_since_last_x | Yards traveled since last second (numeric)|
| force_per_second | Force in Newtons from last second (numeric)|
| is_home | Shows who is home team (1) and away (0) team (numeric boolean) |
| is_defense | Shows what team is on defense (1) yes and (0) no (numeric boolean) |
| uniqueId | Unique id that represents play and game (numeric) |
| playDescription | Description of play (text)
| quarter | Game quarter (numeric) |
| down | Down of play (numeric) |
| yardsToGo | Distance needed for a first down (numeric) |
| team_by_comp_yds| Team rank by cumulative passing yards (numeric)|
| defendersInTheBox | Number of defenders in close proximity to line-of-scrimmage (numeric) |
| numberOfPassRushers | Number of pass rushers (numeric) |
| QB_under_pressure |If a quarter back is under pressure (numeric boolean) |
| gameClock | Time on clock of play (HH:MM:SS) (numeric)
| absoluteYardlineNumber | Distance from end zone for possession team (numeric) |
| epa | Expected points added on the play, relative to the offensive team. Expected points is a metric that estimates the average of every next scoring outcome given the play's down, distance, yardline, and time remaining (numeric) |
| playResult | Net yards gained by the offense, including penalty yardage (numeric) |
| RB | How many running backs in play (numeric)|
| TE | How many tight ends in play (numeric) |
| WR | How many wide receivers in play (numeric) |
| DL | How many defensive linemen in play (numeric) |
| LB | How many linebackers in play (numeric) |
| DB | How many running backs in play (numeric) |
| EMPTY | Offensive formation with no running backs in the backfield (numeric boolean)|
| I_FORM | Offensive formation with two running backs in the backfield one behind the other (numeric boolean)|
| JUMBO | Offensive formation with an extra tight end at the expense of a wide receiver (numeric boolean) |
| PISTOL | Offensive formation where quarterback is in shotgun and a running back behind quarterback (numeric boolean) |
| SHOTGUN | Offensive formation where quarterback is 5-7 yards behind center (numeric boolean) |
| SINGLEBACK | Offensive formation where there is a single running back (numeric boolean) |
| WILDCAT | Offensive formation where the football is snapped to a player other than the quarterback (numeric boolean) |
| four_three | Defensive formation where there are four defensive linemen and three linebackers (numeric boolean) |
| three_four | Defensive formation where there are three defensive linemen and four linebackers (numeric boolean) |
| nickel | Defensive formation where there are five defensive backs (numeric boolean) |
| dime | Defensive formation where there are six defensive backs (numeric boolean) |
| closest_dist | Closest defender distance to the attended receiver on a given pass play (numeric)
| closest_x | Closest x coordinate to the attended receiver for a pass play (numeric)
| closest_y | Closest y coordinate to the attended reviver for a pass play (numeric)

![image](https://user-images.githubusercontent.com/62911364/102654734-b1164c00-4136-11eb-875a-39204b957eb4.png)
<<h3 align = "center">Figure 1</h3>

## Target Variable
| Target | Definition |
| --- | --- |
| pass_stopped | Whether a pass is completed or incomplete including interceptions (numeric boolean) |

</details>

## Teams Rank by Total Completed Passing Yards for 2018
<details>
  <summary>Rank</summary>

| **Team** | **Rank** |
| --- | --- |
| TB | 1 |
| PIT | 2 |
| KC | 3 |
| ATL | 4 |
| LA | 5 |
| GB | 6 |
| PHI | 7 |
| NE | 8 |
| NYG | 9 |
| CLE | 10 |
| IND | 11 |
| HOU | 12 |
| SF | 13 |
| OAK | 14 |
| CAR | 15 |
| MIN | 16 |
| NO | 17 |
| LAC | 18 |
| DAL | 19 |
| DET | 20 |
| CHI | 21 |
| CIN | 22 |
| DEN | 23 |
| BAL | 24 |
| JAX | 25 |
| NYJ | 26 |
| MIA | 27 |
| WAS | 28 |
| TEN | 29 |
| BUF | 30 |
| ARI | 31 |
| SEA | 32 |

</details>

[back to the top](#section_6)
___

<br>

<a id='section_3'></a>

## Initial Hypotheses:
<details>
  <summary>Hypothesis</summary>

> ### Hypothesis 1: Are passes stopped dependent on offensive formation?
>   - H<sub>0</sub>: There is no dependence between offensive formation and pass stopped.
>   - H<sub>a</sub>: There is a dependence between offensive formation and pass stopped.
>
> ### Hypothesis 2: Are passes stopped dependent on down?
>   - H<sub>0</sub>: There is no dependence between down and pass stopped.
>   - H<sub>a</sub>: There is a dependence between down and pass stopped.
>
> ### Hypothesis 3: Are passes stopped dependent on QB pressure?
>   - H<sub>0</sub>: There is no dependence between QB pressure and pass stopped.
>   - H<sub>a</sub>: There is a dependence between QB pressure and pass stopped.
>
> ### Hypothesis 4: Are passes stopped dependent on how many defenders are in the box?
>   - H<sub>0</sub>: There is no dependence between the number of defenders in the box and pass stopped.
>   - H<sub>a</sub>: There is a dependence between the number of defenders in the box and pass stopped.
>
> ### Hypothesis 5: Are passes stopped dependent on number of DL?
>   - H<sub>0</sub>: There is no dependence between the number of DL and pass stopped.
>   - H<sub>a</sub>: There is a dependence between the number of DL and pass stopped.
>
> ### Hypothesis 6: Are passes stopped dependent on number of LB?
>   - H<sub>0</sub>: There is no dependence between the number of LB and pass stopped.
>   - H<sub>a</sub>: There is a dependence between the number of LB and pass stopped.
>
> ### Hypothesis 7: Are passes stopped dependent on number of DB?
>   - H<sub>0</sub>: There is no dependence between the number of DB and pass stopped.
>   - H<sub>a</sub>: There is a dependence between the number of DB and pass stopped.
>
> ### Hypothesis 8: Are passes stopped dependent on defensive formation(Nickel)?
>   - H<sub>0</sub>: There is no dependence between Nickel formation and pass stopped.
>   - H<sub>a</sub>: There is a dependence between Nickel formation and pass stopped.
>
> ### Hypothesis 9: Are passes stopped dependent on defensive formation(Dime)?
>   - H<sub>0</sub>: There is no dependence between Dime formation and pass stopped.
>   - H<sub>a</sub>: There is a dependence between Dime formation and pass stopped.
>
> ### Hypothesis 10: Are passes stopped dependent on defensive formation(4-3)?
>   - H<sub>0</sub>: There is no dependence between 4-3 formation and pass stopped.
>   - H<sub>a</sub>: There is a dependence between 4-3 formation and pass stopped.
>
> ### Hypothesis 11: Are passes stopped dependent on defensive formation(3-4)?
>   - H<sub>0</sub>: There is no dependence between 3-4 formation and pass stopped.
>   - H<sub>a</sub>: There is a dependence between 3-4 formation and pass stopped.
</details>

[back to the top](#section_6)
___

<br>

<a id='section_4'></a>

## Project Plan: Breaking it Down

>- Acquire
>    - Acquire data from csv
>    - Convert into a pandas dataframe
>    - Summarize the data
>    - Plot distribution
>    - Create a ```acquire_nfl.py``` to automate the process
>
>- Prepare
>    - Handle missing and null values
>    - Address data that could mislead models
>    - Create features
>    - Scale the data
>    - Split data into train, validate, test
>    - Create a ```prep_nfl.py``` to automate the process
>
>- Explore
>    - Plot correlation values of all variables
>    - Test each hypothesis
>    - Document and consider the results for modeling
> 
>- Model and Evaluation
>    - Set the baseline
>    - Model using different Classification algorithms: LogisticRegression, KNN, Random Forest, Gradient Boost
>    - Evaluate on train
>    - Evaluate on validate
>    - Evaluate best model to test
>    - create a ```model.py``` to automate the process
>
>- conclusion
>    - summarize findings
>- provide next steps


[back to the top](#section_6)

___

<br>

<a id='section_5'></a>

## How to Reproduce

>1. Download original data csv from [here](https://www.kaggle.com/c/nfl-big-data-bowl-2021/overview)
>2. Install [prepare.py](insert link), [explore.py](insert link) and [model.py](insert link) into your working directory.
>3. Run a jupyter notebook importing the necessary libraries and functions.
>4. Follow along in main_notebook.ipynb or forge your own exploratory path. 

[back to the top](#section_6)

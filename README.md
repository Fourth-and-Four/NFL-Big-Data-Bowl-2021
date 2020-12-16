<a id='section_6'></a>

<img src="https://cdn.hipwallpaper.com/i/66/61/cb1GgL.jpg" width="1000">

<h1 align = "center">NFL-Big-Data-Bowl-2021</h1>
<p align = "center">Authors: Austin Aranda, George Arredondo, Angel Gomez, Gilbert Noriega</p>

[About the Project](#section_1) || [Data Dictionary](#section_2) ||  [Initial Hypotheses](#section_3) || [Project Plan](#section_4) || [How to Reproduce](#section_5)

<br>

<a id='section_1'></a>
## About the Project: 
> - Pending
___

<br>

>*Acknowledgement:The dataset was provided by kaggle.com, originally sourced by nextgenstats.nfl.com* 

___

<br>

## Goals
> Our goal for this project is to create a classification model that will accuractely predict whether the defense will stop a pass from being completed during the NFL 2018 regular season. We will deliver the following in a github repository: 
>
> - A clearly named final notebook. This notebook will be what will contain plenty of markdown documentation and cleaned up code.
> - A README that explains what the project is, how to reproduce the work, and our notes from project planning
> - Python modules that automate the data acquisistion, preparation and modeling process. These modules will be imported and used in the final notebook.

[back to the top](#section_6)

___

<br>

<a id='section_2'></a>
## Data Dictionary

| Feature | Definition |
| --- | --- |
| quarter | Game quarter (numeric) |
| down | Down of play (numeric) |
| yardsToGo | Distance needed for a first down (numeric) |
| team_by_comp_yds| Team rank by cumulative passing yards (numeric)|
| defendersInTheBox | Number of defenders in close proximity to line-of-scrimmage (numeric) |
| numberOfPassRushers | Number of pass rushers (numeric) |
| QB_under_pressure |If a quarter back is under pressure (numeric boolean) |
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

| Target | Definition |
| --- | --- |
| pass_stopped | Whether a pass is completed or incomplete including interceptions (numeric boolean) |

## Teams By Completed Passing Yards
| Team | Ranknig By Passing Yards Completed |
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

[back to the top](#section_6)
___

<br>

<a id='section_3'></a>
## Initial Hypotheses:

> ### Hypothesis 1: Are passes stopped dependent on Offensive Formation?
>   - H<sub>0</sub>: There is no dependence between Offensive Formation and pass stopped
>   - H<sub>a</sub>: There is a dependence between Offensive Formation and pass stopped
>
> ### Hypothesis 2: Are passes stopped dependent on Down?
>   - H<sub>0</sub>: There is no dependence between Down and pass stopped
>   - H<sub>a</sub>: There is a dependence between Down and pass stopped
>
> ### Hypothesis 3: Are passes stopped dependent on QB Pressure?
>   - H<sub>0</sub>: There is no dependence between QB Pressure and pass stopped
>   - H<sub>a</sub>: There is no dependence between offensive formation and pass stopped
>
> ### Hypothesis 4: Are passes stopped dependent on how many Defenders are In The Box?
>   - H<sub>0</sub>: There is no dependence between the number of defenders in the box and pass stopped
>   - H<sub>a</sub>: There is a dependence between the number of defenders in the box and pass stopped
>
> ### Hypothesis 5: Are passes stopped dependent on number of DL?
>   - H<sub>0</sub>: There is no dependence between the number of DL and pass stopped
>   - H<sub>a</sub>: There is a dependence between the number of DL and pass stopped
>
> ### Hypothesis 6: Are passes stopped dependent on number of LB?
>   - H<sub>0</sub>: There is no dependence between the number of LB and pass stopped
>   - H<sub>a</sub>: There is a dependence between the number of LB and pass stopped
>
> ### Hypothesis 7: Are passes stopped dependent on number of DB?
>   - H<sub>0</sub>: There is no dependence between the number of DB and pass stopped
>   - H<sub>a</sub>: There is a dependence between the number of DB and pass stopped
>
> ### Hypothesis 8: Are passes stopped dependent on defensive formation(Nickel)?
>   - H<sub>0</sub>: There is no dependence between Nickel formation and pass stopped
>   - H<sub>a</sub>: There is a dependence between Nickel formation and pass stopped
>
> ### Hypothesis 9: Are passes stopped dependent on defensive formation(Dime)?
>   - H<sub>0</sub>: There is no dependence between Dime formation and pass stopped
>   - H<sub>a</sub>: There is a dependence between Dime formation and pass stopped
>
> ### Hypothesis 10: Are passes stopped dependent on defensive formation(4-3)?
>   - H<sub>0</sub>: There is no dependence between 4-3 formation and pass stopped
>   - H<sub>a</sub>: There is a dependence between 4-3 formation and pass stopped
>
> ### Hypothesis 11: Are passes stopped dependent on defensive formation(3-4)?
>   - H<sub>0</sub>: There is no dependence between 3-4 formation and pass stopped
>   - H<sub>a</sub>: There is a dependence between 3-4 formation and pass stopped

[back to the top](#section_6)
___

<br>

<a id='section_4'></a>
## Project Plan: Breaking it Down

>- acquire
>    - acquire data from csv
>    - turn into a pandas dataframe
>    - summarize the data
>    - plot distribution
>
>- prepare
>    - address data that could mislead models
>    - create features
>    - scale the data
>    - split into train, validate, test
>    - create a prepare.py to automate the process
>
>- explore
>    - plot correlation values of all variables
>    - test each hypothesis
>    - document and consider the results for modeling
> 
>- model and evaluation
>    - set the baseline
>    - try different algorithms: LogisticRegression, KNN, Random Forest, Gradient Boost
>    - evaluate on train
>    - evaluate on validate
>    - select best model and test to verify
>    - create a model.py to automate the process
>
>- conclusion
>    - summarize findings
>- provide next steps


[back to the top](#section_6)

___

<br>

<a id='section_5'></a>
## How to Reproduce

>1. Download original data csv from [here](insert link)
>2. Install [prepare.py](insert link), [explore.py](insert link) and [model.py](insert link) into your working directory.
>3. Run a jupyter notebook importing the necessary libraries and functions.
>4. Follow along in main_notebook.ipynb or forge your own exploratory path. 

[back to the top](#section_6)
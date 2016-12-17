# College Major Recommender System

A college major recommendation system to make incoming undergraduate students' lives easier.

Students are provided a list of recommended majors based on their answers to a short, 20 question quiz capturing information about their interests and career goals. Information on income and employment statistics for a given major is included along with the recommended majors.

The final product is deployed as a web app which can be found here:

www.torrez.tech

For an in-depth look into the motivation and methodology of the project, read on.

## A Quick Thank You
This project was completed as my capstone project for the Galvanize Data Science Immersive and without the help of my instructors and classmates there is no way I could have completed this in the mere two weeks we had to work on it.

And, of course, ***thank you*** for visiting and checking out my project.


## Problem Statement

### Motivation
Two important choices face first time college students: where will they go to college and what will they major in? An entire industry has been built around the first question: consultants are now paid over $50/hr (that works out to about $100,000 a year) helping students pick the “right” college for them. In addition, most students have the chance to work one-on-one with a college counselor at their high school to guide them through the process. However, there exists far fewer resources for guiding students to the field that will be the best fit for them. The saturation of resources on only one of those two problems is unfortunate due to the fact that it has become more apparent in recent years that where you go to college isn’t as important as we have led ourselves to believe ([this book](https://www.hachettebookgroup.com/titles/frank-bruni/where-you-go-is-not-who-youll-be/9781455532704/) and [this book](http://www.billderesiewicz.com/books/excellent-sheep) have great discussions of the issue).

**I have built a college major recommendation system to address the question: what should I pick for my college major?**

### The Intended Audience and a Few Caveats
It is important to first understand the audience for this system: those who have little to no idea what they would like to do in their working life. Those who have wanted to be doctors, or lawyers, or astronauts since they were young won't find find this tool as useful. But, for those who enter school with undecided/exploratory majors or for who would like to just explore some alternate ideas because they aren't completely sure of their major, this tool offers a good starting place.

The last point deserves some emphasis: this is only a starting place. It is not meant to replace much more rigorous assessments and theories that have been validated over decades (the [Strong Interest Inventory](https://en.wikipedia.org/wiki/Strong_Interest_Inventory) and the work of [John Holland](https://en.wikipedia.org/wiki/Holland_Codes) are good places to start in understanding the current state of knowledge in this area).  Rather, it provides a short, quick experience that is accessible to everyone and can point them in some new directions. It is not meant to replace the great work done by college/career counselors, but would ideally be used in conjunction with expert advice.

One of the difficulties in recommending a major for a student is how disparate, and sometimes even conflicting, the things that must be taken into account for each individual student are. They may love art, but also want to be making $100,000 a year by the time they are thirty. They may want to major in pre-med, but also have a normal work life balance both in college and later in life. I believe that this is part of the reason that there are so few resources out there for picking a major: there are just too many potentially conflicting signals to take into account. There may be an article addressing how to pick based on your passions, or one advising you about the incomes of different majors, or one that suggests that your Myers-Briggs type is what will decide whether that field you are considering is a good fit for you, but they are rarely synthesized into one place. Even when they are (such as this [excellent site](http://www.bestcolleges.com/resources/choosing-a-major/)), the user is required to parse and digest an overwhelming amount of information.

### The Final Goal
This recommender system focuses on two main areas: the passions/interests of students and their desired future income/career aspirations.  Future work will attempt to incorporate more sources of data.

<br>
## Data

### The Ideal
The ideal type of data for a recommender system contains information about how well a product fits the needs of various users. Most commonly, this comes in the form of ratings. For example, the ratings of movies/shows on Netflix allow the company to make recommendations to you based on both how similar the characteristics of other movies are to the characteristics of movies that you enjoy (content-based filtering) and how much users who have similar taste to you liked movies you haven't seen yet (collaborative filtering).

However, sadly, a database of how people would rate the fit of their undergraduate majors doesn't exist. Even if it did, there would still be difficulties with the data since a single person would generally only rate a single major, as it costs much more money and time to obtain as many majors as the number of movies or television shows you have watched on Netflix!


### User Interests Data
That said, many colleges have short quizzes that incoming students can take that capture information about the interests and passions of the student, and then suggest majors/departments the student should explore.  The first part of the data used in this project is based on a few such quizzes (the main one I used is [here](http://www.luc.edu/undergrad/academiclife/whatsmymajorquiz/#) and another is [here](http://www.marquette.edu/explore/choose-your-major/quiz.php)).

An issue with these information sources is that I do not have access to the recommendations returned for all the users that have taken the quiz.

**To remedy this fact, I built a bot/script that can take the quiz a large number of times, and then record the predictions.**

I made one important change to the quiz.  Instead of returning a specific major, it was modified to return a probability distribution. This distribution can be interpreted as a degree of belief that a given user is interested in a given field of study. For example

|Field of Study                 | Degree of Belief        |
|:-----------------------------:|:-----------------------:|
| Business and Communication    | 0.15                    |
| Creative Arts                 | 0.30                    |
| Math Sciences and Engineering | 0.20                    |
| Public Service Law and Policy | 0.23                    |
| Social Sciences               | 0.12                    |

Each question in the quiz is tied to certain majors (meaning, if the user answers yes to the question, then they might be interested in those majors) each of which falls into one of the above fields. Therefore, based on their answers, we can create a distribution of how likely they are to be interested in a given field. I then labeled each set of answers produced by my bot with a field of study, sampling the labels from the distribution produced by the quiz. I believe that this method captures the extreme variability in picking a major based on a survey: just because a student answers the questions a certain way doesn't ***guarantee*** that they will be a certain major. They may be most likely to lean a certain way, but we should leave open the possibility that they may still discover a field they hadn't considered yet.

### Projected Income and Employment Rates of College Majors
The second part of the data was much easier to obtain.  I wanted to give the user an idea of the income and employment rates of a selection of popular majors. I utilized the job/income data that FiveThirtyEight used in their [article](http://fivethirtyeight.com/features/the-economic-guide-to-picking-a-college-major/)  about the earning potential of majors.  The data can be found [here](https://github.com/fivethirtyeight/data/tree/master/college-majors). This data was originally collected via the American Community Survey (ACS) from 2010-2012.  I've  attempted to find more current data, but unfortunately the ACS appears to have removed the major variable code from their surveys.

<br>
## The Modeling

I utilized the scikit-learn implementation of a random forest model to predict the probabilities of a user's interest in a given major.

### The Machine Learning in Context aka What was the Model Actually Used For
It is important to keep in mind here that the model was used mainly to test how important keeping all the questions in the quiz was. It was also used to speed up the calculation of probabilities as random forests may take a long time to train, but they have very short prediction run times.

Why reduce the number of questions in the quiz at all?  This makes it easier for for the user to use this tool. Ideally, I wanted to reduce the quiz to 10 questions.  So, in this case, I wasn't overly concerned with the performance of the model, except to confirm that the performance didn't change appreciably from when it was run with the full complement of questions to when it was run with only the selected 10 questions.

The Random Forest model is a perfect choice for this task as it can build a diverse set of learners that will try different combinations of questions on random bootstrap samples of the data, preventing the model from getting fixated on only one question or consistently building decision paths with questions asked in the same order. This will give us more insight into how important questions really are.

### Quick Note on Parameters
Most of the default parameters worked well in this case. I didn't want to limit the depth of the trees here so I could capture all interactions between questions, something you miss out on by limiting tree depth. I also didn't need a large number of estimators, since we aren't too concerned about maximizing the ability of the model to actually predict things.

One important note is that I did balance the class weights, as when I tested it without this setting, the model *never* predicted someone would be interested in the creative arts. While that may be semi reasonable from an economic standpoint (hence, art majors are few and far between), I don't want to leave my users unable to ever see art as a possible choice.

### Evaluating and Picking the Final Set of Questions

Accuracy metrics are extremely low, but that is often the case when predicting multiple classes. In this project, especially, we would expect this since the original labeled data was already extremely noisy. Log loss is interesting as it is fairly low (though what qualifies as "very low" is definitely up for debate), which was a little unexpected considering I expected my model to be horrible at actually making predictions. However, considering what log loss measures (large penalty for being really sure about a wrong classification), this actually makes some sense. My model inherently is never that sure about its predictions and this lack of commitment prevents it from predicting a high probability of any one class, but incorrect. Basically, it is unsure all the time and log loss only really blows up only when you're sure about something, which this model never is.

That being said, there was only one aspect of evaluation I was concerned with here: did the performance of the model stay the same from using the bot's answers to all 35 of the original questions vs. using the bot's answers to a subset of 10 questions? If we don't see a change in performance, it can help validate the assumption that using less questions doesn't make the model less able to predict the fields of study a user might be interested in.

To pick the final 10 questions used in the survey, I first looked at the feature importances reported from the random forest. The top 4 questions (as ranked by feature importance) were clear cut, but the subsequent feature importances level off to be relatively constant. At that point, I started picking questions that were a little less direct (direct ex: "I like science" vs. indirect: "I can work on projects very carefully and thoroughly, with patience and determination.") for a more subtle touch to the survey. This is a common survey technique, and while I can most definitely *not* comment on its validity, I do think it is a common sense thing to do.

Thankfully, there was no appreciable change in performance from predicting with the full question set to predicting with the 10 question subset. Here are the evaluation metrics for the model trained on the full question set vs. the model trained on the 10 question subset (all metrics were measured using a hold-out validation set):

#### Full Question Set Metrics
|                               | precision | recall | f1-score |
|:-----------------------------:|:---------:|:------:|:--------:|
| Business and Communication    | 0.27      | 0.18   | 0.21     |
| Creative Arts                 | 0.10      | 0.45   | 0.17     |
| Math Sciences and Engineering | 0.44      | 0.14   | 0.21     |
| Public Service Law and Policy | 0.25      | 0.14   | 0.18     |
| Social Sciences               | 0.22      | 0.46   | 0.30     |
|                               |           |        |          |
| Weighted Average              | 0.31      | 0.22   | 0.22     |

| Log Loss |
|:--------:|
| 1.577995 |


#### 10 Question Subset Metrics
|                               | precision | recall | f1-score |
|:-----------------------------:|:---------:|:------:|:--------:|
| Business and Communication    | 0.27      | 0.18   | 0.22     |
| Creative Arts                 | 0.10      | 0.46   | 0.17     |
| Math Sciences and Engineering | 0.44      | 0.14   | 0.21     |
| Public Service Law and Policy | 0.25      | 0.14   | 0.18     |
| Social Sciences               | 0.22      | 0.45   | 0.30     |
|                               |           |        |          |
| Weighted Average              | 0.31      | 0.22   | 0.22     |

| Log Loss |
|:--------:|
| 1.577585 |


### Incorporating Career Outcomes

I decided to focus on two aspects of possible careers: how secure are jobs in the field and how much money can you make in that field? These two things were the most common topics I discussed with graduating students during my time as a high school teacher. Some students were very concerned with being absolutely sure they would have a job; some students only cared about how much money they could make. For each user that used my survey, I wanted to capture what I called their ***risk tolerance*** and their ***income desire***.

#### Risk

There were three things that I felt could describe a risky major:
 1. There is a higher rate of being unemployed than you would usually expect across all majors.
 2. There is a lower rate of being full-time employed than you would usually expect across all majors.
 3. If you are unlucky enough to be paid near the low end of what your major is paid, is it lower that what you would usually expect across all majors.

To calculate a metric that captures those ideas, I took the difference for the value of each one of those data points (unemployment rate, full-time employment rate, and the income at the 25th percentile) for a given major from the median value for that data point for all majors. The equation, in pseudo-code, looks like this:

```
ur = unemployment_rate, ftr = full_time_employment_rate, p25th_income = income at 25th percentile

risk_rating = (ur - ur.median()) + (ftr.median() - ftr) + (p25th_income.median() - p25th_income)
```

The higher the risk rating, the more risky the major as that would correlate to unemployment rates higher than normal, full-time employment rates lower than normal, and p25th income lower than normal.

#### Income Gain

There were two things that I felt could describe a major that had a high potential gain:
 1. The typical (median) income is higher than the median income across all majors.
 2. If you are lucky enough to be paid near the high end of what your major is paid, is it higher than what you would usually expect across all majors.

To calculate a metric that captures those ideas, I took the difference for the value of each one of those data points (median income and the income at the 75th percentile) for a given major from the median value for that data point for all majors. The equation, in pseudo-code, this looks like:

```
gain_rating = (median_income - median_income.median()) + (p75th_income - p75th_income.median())
```

The higher the gain rating, the more money that major would make than is typical, as that would correlate to higher incomes at both the normal income and the upper end of incomes.

### Putting It Together

Now that I had a way to measure the risk and income gain of a major, I needed a way to incorporate the users risk tolerance and income desire. I scraped some questions from a career motivation [quiz](http://www.queendom.com/tests/access_page/index.htm?idRegTest=3154#n) that related to this and came up with a simple scale.

There were 5 questions relating to risk vs. security. For each question, there was a positive response (meaning they were tolerant of risk) and a negative response. Each positive response was worth 0.2, meaning that a user's risk tolerance score ranged from 0-1; the higher the score, the more comfortable they were with risk in their future career.

There were 5 more questions I added relating to income desire. Since everyone will answer "yes" to making more money, I decided to have users decide between helping the world and income. This is definitely not a perfect methodology, but it does force the user to make trade-offs, which is a common technique in career motivations surveys. The same scoring system as the one for risk tolerance was used.

By answering these additional 10 questions I could then weight each major by how well it matched their career goals. The final metric I used to calculate this weight, in pseudo-code:

```
major_weight = (risk_tolerance_score * risk_rating) + (income_desire_score * gain_rating)
```

### Final Workflow

The final step of modeling was to synthesize each individual piece into one workflow. Using the user's answers to the first 10 questions about their interests, the random forest model produced the probabilities that a user was interested in each field of study. Each major in my data had been mapped to these field of studies so now each major had a degree of belief (probability of interest) associated with it. I could then use the user's answers to the second set of 10 questions to find the major weights (which describes how good of a match a major is based on their desired career outcomes) and multiply the degree of belief by the weight to produce a final degree of belief for each individual major. I then show the user the top 20 majors that match their input answers, along with the related income and employment statistics, to give them some new areas to consider.

<br>
## The Product

The ultimate goal of this project was to deploy it in a way that made it accessible to any student with internet access. HTML and CSS Bootstrap templates were used to improve the look the final product. Flask was used for the server backend, and the final product was to deployed on an AWS EC2 instance. Check out the final product at www.torrez.tech

<br>
## Future Work

This project exists mostly as a proof of concept and there are many things that could be done to improve the recommendations and make it a more useful tool.

### Feedback to User

The most glaring miss of this project is the feedback the user receives when they finish the quiz. Though the app does output a list of 20 majors for the user to consider, there is no information about ***why*** these majors have been recommended for them. One thing I have found when showing the app to people in person is that I can usually explain an initially strange seeming result by looking at their answers. This would be the most important and useful addition to the app.

### Improved Survey Questions

All the survey questions used in this project come from non-validated surveys and quizzes. Incorporating a properly validated set of survey questions (to ensure I am actually capturing the information about my user that I think I am) could turn this into a tool that academic and career counselors might feel comfortable pointing their clients to in order to start their explorations. Having properly validated questions would also improve this project with respect the ideas of equal opportunity and accessibility for all students: those users that don't have access to a counselor would have confidence that the recommendations they are receiving represent what they might receive if they did have access to a trained professional.

### Further Evaluation

Confirming that the recommendations being made are actually a good fit for the user is one of the most essential parts of recommendation systems. Capturing whether a college major is a good fit for a person, or not, is something that would require a years-long longitudinal study if I did it on my own. Incorporating data from sites that tell you about how many students are still using their [major](http://www.studentsreview.com/still_in_field_by_major.php3) or partnering with universities/colleges to utilize their data are possible ways I could start to evaluate this project.

## Thank You

If you managed to read this far...

<img src="images/fun/dwightthankyou.gif">

<br>

<img src="images/logos/python.png" width="120">
<img src="images/logos/jupyter.png" width="120">
<img src="images/logos/sklearn.png" width="120">
<img src="images/logos/flask.png" width="120">
<img src="images/logos/bootstrap.png" width="120">
<img src="images/logos/jquery.png" width="120">
<img src="images/logos/aws.png" width="120">

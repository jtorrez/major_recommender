# College Major Recommender System

A college major recommendation system to make incoming undergraduate students' lives easier.

Students are given a list of recommended majors based on their answers to a short, 20 question quiz capturing information about their interests and career goals. Information on income and employment statistics for a given major is included along with the recommended majors.

The final product is deployed as a web app which can be found here:

[link coming]

For an in-depth look into the motivation and methodology of the project, read on.

## A Quick Thank You
This project was completed as my capstone project for the Galvanize Data Science Immersive and without the help of my instructors and classmates there is no way I could have completed this in the mere two weeks we had to work on it. Special shout out to Matt Drury, my advisor on the project, for all the guidance and brainstorming sessions.

And, of course, ***thank you*** for visiting and checking out my project.

## The Tools

<img src="images/logos/python.png" width="120">
<img src="images/logos/jupyter.png" width="120">
<img src="images/logos/sklearn.png" width="120">
<img src="images/logos/flask.png" width="120">
<img src="images/logos/bootstrap.png" width="120">
<img src="images/logos/jquery.png" width="120">
<img src="images/logos/aws.png" width="120">

<br>
## The Problem

### The Motivation
Two important choices face first time college students: where will they go to college and what will they major in? An entire industry has been built around the first question: tutors are now paid over $50/hr (that’s 100k a year if you’re counting…) helping students get into and pick the “right” college for them. In addition, most students have the chance to work one-on-one with a college counselor at their high school to guide them through the process. However, there exists far fewer resources for guiding students to the field that will be the best fit for them. The saturation of resources on only one of those two problems in unfortunate due to the fact that it has become more apparent in recent years that where you go to college isn’t actually that important ([this book](https://www.hachettebookgroup.com/titles/frank-bruni/where-you-go-is-not-who-youll-be/9781455532704/) and [this book](http://www.billderesiewicz.com/books/excellent-sheep) have great discussions of the issue).

**In order to address the question “what should I pick for my college major?”, I have built a college major recommendation system.**

### The Audience and a Few Caveats
It is first important to understand the audience for this system: those who really have no idea what they would like to do. Those who have wanted to be doctors, or lawyers, or astronauts since they were young won't find this tool to be of much use. But for those who enter school as undecided/exploratory majors or for those who would like to just explore some alternate ideas because they aren't completely sold on their major, this tool can offer a good starting place.

That is the other important component to understand about this system: it is only a starting place. It is also not meant to replace much more rigorous assessments and theories that have been thoroughly validated over decades (the [Strong Interest Inventory](https://en.wikipedia.org/wiki/Strong_Interest_Inventory) and the work of [John Holland](https://en.wikipedia.org/wiki/Holland_Codes) are important places to start), but rather to provide a short, quick tool that is accessible to everyone and can point them in some new directions. It is also not meant to replace the great work done by college/career counselors and would ideally be used in conjunction with their expert advice.

One of the difficulties in recommending a major for a student is how disparate, and sometimes even conflicting, the things you have to take into account for each individual student are. They may love art, but also want to be making 100k a year by the time they are 30. They may want to go pre-med, but also have a normal work life balance both in college and later in life. I believe that this is part of the reason that are so few resources out there for picking a major: there are just too many things to take into account. There may be an article addressing how to pick based on your passions, or one advising you about the incomes of different majors, or one that suggests that your Myers-Briggs type is what will really decide whether that field you are considering is a good fit for you, but they are rarely synthesized into one place. Even when they are (such as this [excellent site](http://www.bestcolleges.com/resources/choosing-a-major/)), they still require you to go through and parse an overwhelming amount of information.

### The Final Goal
The recommender system I built focused on two main areas (as a proof of concept): the passions/interests of students and their desired future income/career aspirations.

<br>
## The Data

### The Ideal Data
The ideal type of data for a recommender system is a set of information about how well a certain product fit the needs of a user. Most commonly, this comes in the form of ratings. For example, the ratings of movies/shows on Netflix allows the company to make recommendations to you based on both how similar the characteristics of other movies are to the characteristics of movies that you enjoy (content-based filtering) and how much users who have similar taste to you liked movies you haven't seen yet (collaborative filtering).

However, sadly, a database of how people would rate the fit of their undergraduate majors doesn't exist. Even if it did, there would still be difficulties with the data since a single person would rate, most of the time, a single major as it costs much more money to obtain as many majors as the number of movies/shows you have watched on Netflix!


### User Interests Data
That being said, many colleges have short quizzes that incoming students can take that capture information about the interests and passions of the student and then suggest majors/departments the student should explore. Capturing those student characteristics is exactly what I was after, so the first part of the data is based on a few such quizzes (the main one I used [here](http://www.luc.edu/undergrad/academiclife/whatsmymajorquiz/#) and another [here](http://www.marquette.edu/explore/choose-your-major/quiz.php)). The only issue is that I did not have access to the predictions that the quiz has output for all the users that have taken the quiz.

**To remedy that fact, I built a bot/script that could take the quiz for me a large amount of times (10,000 times to be exact) and then record the predictions creating a set of data to work with.**

One important change I made to the quiz was the result it output. Instead outputting a specific major, it instead output a probability distribution, though it is better to think of it as my degree of belief that a user is interested in a given field of study, of how likely a student was to be interested in a given field of study. An example of that output:

|Field of Study                 | Degree of Belief        |
|:-----------------------------:|:-----------------------:|
| Business and Communication    | 0.15                    |
| Creative Arts                 | 0.30                    |
| Math Sciences and Engineering | 0.20                    |
| Public Service Law and Policy | 0.23                    |
| Social Sciences               | 0.12                    |

How in the world did I get such a distribution? Well, each question in the quiz is tied to certain majors (meaning, if the user answers yes to the question, then they might be interested in those majors) each of which falls into one of the above fields. Therefore, based on their answers, we can create a distribution of how likely they are to be interested in a given field. I then labeled each set of answers produced by my bot with a field of study, sampling the labels from the distribution produced by the quiz. I believe that this method captures the extreme variability in picking a major based on a survey: just because a student answers the questions a certain way doesn't ***guarantee*** that they will be a certain major. They may be most likely to lean a certain way, but we should leave the open the possiblity that they may still discover a field they haven't considered yet.

### Projected Income and Employment Rates of College Majors
The second part of the data was much easier to obtain as I simply wanted to give the user an idea of the income and employment rates of a selection of popular majors. I utilized the job/income data that FiveThirtyEight used in their article about the earning potential of majors ([read it here](http://fivethirtyeight.com/features/the-economic-guide-to-picking-a-college-major/)) which can be found [here](https://github.com/fivethirtyeight/data/tree/master/college-majors). The data was originally found via the American Community Survey (ACS) from 2010-2012. I attempted to find more current data, but unfortunately the ACS appears to have removed the major variable code from their surveys or I simply am not good enough at navigating their data portal to find it.

<br>
## The Modeling

I utilized the scikit-learn implementation of a random forest model to predict the probabilities of a user's interest in a given major.

### The Machine Learning in Context aka What was the Model Actually Used For
It is important to keep in mind here that the model was used mainly to test how important keeping all the questions in the quiz was. It was also used to speed up the calculation of probabilities as random forests may take a long time to train, but they have very short prediction run times.

Why reduce the number of questions in the quiz at all? Simply to make it easier for for the user to use this tool. Ideally, I wanted to reduce the number of questions to 10 questions and believed that I could without much issue, but using a model to check this assumption was useful. So, in this case, I wasn't overly concerned with the performance of the model, except to confirm that the performance didn't change significantly from when it was run with the full compliment of questions to when it was run with only the selected 10 questions.

The Random Forest model is a perfect pick for this job as it can build a diverse set of learners that will try different combinations of questions on random bootstrap samples of the data, preventing the model from getting fixated on only one question or consistently building decision paths with questions asked in the same order. This will give us more insight into how important questions really are.

### Quick Note on Parameters
Most of the default parameters worked well in this case. I didn't want to limit the depth of the trees here so I could capture all interactions between questions, something you miss out on by limiting tree depth. I also didn't need a large number of estimators, since we aren't too concerned about maximizing the ability of the model to actually predict things.

One important note is that I did for the class weights to be balanced as when I tested it without this setting, the model NEVER predicted someone would be interested in the creative arts. While that may be semi reasonable from a real life standpoint (art majors are few and far between), I don't want to leave my users unable to ever see art as a possible choice.

### Evaluating and Picking the Final Set of Questions

Accuracy metrics are extremely low, but that is often the case when predicting multiple classes. In this project, especially, we would expect this since the original labeled data was already extremely variable. Log loss is interesting as it is fairly low (though what qualifies as "very low" is definitely up for debate), which was a little unexpected considering I expected my model to be horrible at actually making predictions. However, considering what log loss measures (large penalty for being really sure about a wrong classification), this actually begins to make more sense. My model inherently is never that sure about it's predictions and this lack of commitment prevents it from making high probability, but incorrect, classifications. Basically, it is kinda wrong all the time and log loss only really blows up only when you're sure about something which my model never is. Interesting example of the power and limitations of log loss.  

That being said, there was only one aspect of evaluation I was concerned with here: did the performance of the model stay the same from using the bot's answers to all 35 of the original questions vs. using the bot's answers to a subset of 10 questions? If we don't see a change in performance, it can help validate the assumption that using less questions doesn't make the model less able to predict the fields of study a user might be interested in.

To pick the final 10 questions used in the survey, I first looked at feature importance. The top 4 questions (as ranked by feature importance) were clear cut, but after that the feature importances level off to relatively equal. At that point, I started picking questions that were a little less direct (direct ex: "I like science" vs. indirect: "I can work on projects very carefully and thoroughly, with patience and determination.) for a little subtler touch to the survey. This is a common survey technique and while I can most definitely NOT make any comment on the validity (I'd have to spend possibly years validating good survey questions) of that, I do think it is a common sense thing to do in order to capture more subtle information about my user.

Thankfully, there was no change in performance from predicting with the full question set to predicting with the 10 question subset. Here are the evaluation metrics for the model trained on the full question set vs. the model trained on the 10 question subset (all metrics were measured using a hold-out validation set):

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

I decided to focus on two aspects of possible careers: how secure are jobs in the field and how much money can you make in that field? These two things were the most common topics I discussed with graduating students during my time as a high school teacher. Some students were very concerned with being absolutely sure they would have a job; some students only cared about how much money they could make. For each user that used my survey, I wanted to capture what I called their ***risk tolerance*** and their ***income desire***. But first, I needed to quantify exactly how risky and how much money there was to be gained for each given major in my data.


### Developed Metrics

Quick aside here: I accounted for differing scales (ex: unemployment rate is a percentage from 0-100 and income is in dollars from 0-unlimited) by normalizing all data to a 0-1 scale. Those calculations can be found in the source code, but have been left out here for ease of reading.

#### Risk

There were three things that I felt could describe a risky major:
 1. There is a higher rate of being unemployed than you would usually expect across all majors.
 2. There is a lower rate of being full-time employed than you would usually expect across all majors.
 3. If you are unlucky enough to be paid near the low end of what your major is paid, is it lower that what you would usually expect across all majors.

To calculate a metric that captures those ideas, I took the difference for the value of each one of those data points (unemployment rate, full-time employment rate, and the income at the 25th percentile) for a given major from the median value for that data point for all majors. The equation, in pseudo-code, looks like this:

ur = unemployment_rate, ftr = full_time_employment_rate, p25th_income = income at 25th percentile

risk_rating = (ur - ur.median()) + (ftr.median() - ftr) + (p25th_income.median() - p25th_income)

The higher the risk rating, the more risky the major as that would correlate to unemployment rates higher than normal, full-time employment rates lower than normal, and p25th income lower than normal.

#### Income Gain

There were two things that I felt could describe a major that had a high potential gain:
 1. The typical (median) income is higher than the median income across all majors.
 2. If you are lucky enough to be paid near the high end of what your major is paid, is it higher than what you would usually expect across all majors.

To calculate a metric that captures those ideas, I simply took the difference for the value of each one of those data points (median income and the income at the 75th percentile) for a given major from the median value for that data point for all majors. The equation, in pseudo-code, looks like this:

gain_rating = (median_income - median_income.median()) + (p75th_income - p75th_income.median())

The higher the gain rating, the more money that major would make than is typical, as that would correlate to higher incomes at both the normal income and the upper end of incomes.

### Final Workflow

Now that I had a way to measure the risk and income gain of a major, I needed a way to incorporate the users risk tolerance and income desire. I scraped some questions from a career motivation [quiz](http://www.queendom.com/tests/access_page/index.htm?idRegTest=3154#n) that related to this and came up with a simple scale.

There were 5 questions relating to risk vs. security. For each question, there was a positive response (meaning they were tolerant of risk) and a negative response. Each positive response was worth 0.2, meaning that a user's risk tolerance score ranged from 0-1; the higher the score, the more ok they were with risk in their future career.

There were 5 more questions I added relating to income desire. Since everyone will answer "yes" to making more money, I decided to make them decide between helping the world and income. This is definitely not a perfect methodology, but it does force the user to make trade-offs which is a common technique in career motivations surveys. The same scoring system as the risk tolerance was used.

**to be finished**

<br>
## The Product

The ultimate goal of this project was to deploy it in a way that made it accessible to any student with internet access. That means it was time to get my web dev hat on. Heavily utilizing HTML and CSS Bootstrap templates to make the site look pretty made the final product look much better than my simple web capabilities would actually allow. After building a Flask server backend, the final step was to deploy it on an AWS EC2 instance and buy a fancy domain name. Check out the final product at [www.fancydomainname.com]

<br>

## Future Work

This project exists mostly as a proof of concept and there are many things that could be done to improve the recommendations and make it a more useful tool.

### Feedback to User

The most glaring miss of this project is the feedback the user receives when they finish the quiz. Though the app does output a list of 20 majors for the user to consider, there is no information about ***why*** these majors have been recommended for them. One thing I have found when showing the app to people in person is that I can usually explain an initially strange seeming result by looking at their answers. This would be the most important and useful addition to the app.

### Improved Survey Questions

All the survey questions used in this project come from non-validated surveys and quizzes. Incorporating a properly validated set of survey questions (to ensure I am actually capturing the information about my user that I think I am) could turn this into a tool that academic and career counselors might feel comfortable pointing their clients to in order to start their explorations. Having properly validated questions would also improve this project with respect the ideas of equal opportunity and accessibility for all students: those users that don't have access to a counselor would have confidence that the recommendations they are receiving represent what they might receive if they did have access to a trained professional.

### Further Evaluation

Confirming that the recommendations being made are actually a good fit for the user is one of the most essential parts of recommendation systems. Capturing whether a college major is a good fit for a person, or not, is something that would require a years long longitudinal study if I did it on my own. Incorporating data from sites that tell you about how many students are still using their [major](http://www.studentsreview.com/still_in_field_by_major.php3) or partnering with universities/colleges to utilize their data are possible ways I could start to evaluate this project.

## Thank You

If you managed to read this far...

<img src="images/fun/dwightthankyou.gif">

# College Major Recommender System

Building a college major recommendation system to make incoming undergraduate students' lives easier.

<br>
## The Tools

<img src="images/logos/python.png" width="120">
<img src="images/logos/jupyter.png" width="120">
<img src="images/logos/sklearn.png" width="120">
<img src="images/logos/flask.png" width="120">
<img src="images/logos/bootstrap.png" width="120">
<img src="images/logos/jquery.png" width="120">

<br>
## The Problem

Two important choices face first time college students: where will they go to college and what will they major in? An entire industry has been built around the first question: tutors are now paid over $50/hr (that’s 100k a year if you’re counting…) helping students get into and pick the “right” college for them. In addition, most students have the chance to work one-on-one with a college counselor at their high school to guide them through the process. However, there exists far fewer resources for guiding students to the field that will be the best fit for them. The saturation of resources on only one of those two problems in unfortunate due to the fact that it has become more apparent in recent years that where you go to college isn’t actually that important ([this book](https://www.hachettebookgroup.com/titles/frank-bruni/where-you-go-is-not-who-youll-be/9781455532704/) and [this book](http://www.billderesiewicz.com/books/excellent-sheep) have great discussions of the issue).

**In order to address the question “what should I pick for my college major?”, I have built a college major recommendation system.**

It is first important to understand the audience for this system: those who really have no idea what they would like to do. Those who have wanted to be doctors, or lawyers, or astronauts since they were young won't find this tool to be of much use. But for those who enter school as undecided/exploratory majors or for those who would like to just explore some alternate ideas because they aren't completely sold on their major, this tool can offer a good starting place.

That is the other important component to understand about this system: it is only a starting place. It is also not meant to replace much more rigorous assessments and theories that have been thoroughly validated over decades (the [Strong Interest Inventory](https://en.wikipedia.org/wiki/Strong_Interest_Inventory) and the work of [John Holland](https://en.wikipedia.org/wiki/Holland_Codes) are important places to start), but rather to provide a short, quick tool that is accessible to everyone and can point them in some new directions.

One of the difficulties in recommending a major for a student is how disparate, and sometimes even conflicting, the things you have to take into account for each individual student are. They may love art, but also want to be making 100k a year by the time they are 30. They may want to go pre-med, but also have a normal work life balance both in college and later in life. I believe that this is part of the reason that are so few resources out there for picking a major: there are just too many things to take into account. There may be an article addressing how to pick based on your passions, or one advising you about the incomes of different majors, or one that suggests that your Myers-Briggs type is what will really decide whether that field you are considering is a good fit for you, but they are rarely synthesized into one place. Even when they are (such as this [excellent site](http://www.bestcolleges.com/resources/choosing-a-major/)), they still require you to go through and parse an overwhelming amount of information.

**The recommender system I built focused on two main areas (as a proof of concept): the passions/interests of students and their desired future income/career aspirations.**

<br>
## The Data

The ideal type of data for a recommender system is a set of information about how well a certain product fit the needs of a user. Most commonly, this comes in the form of ratings. For example, the ratings of movies/shows on Netflix allows the company to make recommendations to you based on both how similar the characteristics of other movies are to the characteristics of movies that you enjoy (content-based filtering) and how much users who have similar taste to you liked movies you haven't seen yet (collaborative filtering).

However, sadly, a database of how people would rate the fit of their undergraduate majors doesn't exist. Even if it did, there would still be difficulties with the data since a single person would rate, most of the time, a single major as it costs much more money to obtain as many majors as the number of movies/shows you have watched on Netflix!

That being said, many colleges have short quizzes that incoming students can take that capture information about the interests and passions of the student and then suggest majors/departments the student should explore. Capturing those student characteristics is exactly what I was after, so the first part of the data is based on a few such quizzes (the main one I used [here](http://www.luc.edu/undergrad/academiclife/whatsmymajorquiz/#) and another [here](http://www.marquette.edu/explore/choose-your-major/quiz.php)). The only issue is that I did not have access to either the predictions that the quiz has output for all the users that have taken the quiz.

**To remedy that fact, I built a bot/script that could take the quiz for me a large amount of times (10,000 times to be exact) and then record the predictions creating a set of data to work with.**

One important change I made to the quiz was the result it output. Instead outputting a specific major, it instead output a probability distribution of how likely a student was to be interested in a given field of study. An example of that output:

|Field of Study                 | Probability of Interest |
|:-----------------------------:|:-----------------------:|
| Business and Communication    | 0.15                    |
| Creative Arts                 | 0.30                    |
| Math Sciences and Engineering | 0.20                    |
| Public Service Law and Policy | 0.23                    |
| Social Sciences               | 0.12                    |

How in the world did I get such a distribution? Well, each question in the quiz is tied to certain majors (meaning, if the user answers yes to the question, then they might be interested in those majors) each of which falls into one of the above fields. Therefore, based on their answers, we can create a distribution of how likely they are to be interested in a given field. I then labeled each set of answers produced by my bot with a field of study, sampling the labels from the distribution produced by the quiz. I believe that this method captures the fact the extreme variability in picking a major based on a survey: just because a student answers the questions a certain way doesn't *guarantee* that they will be a certain major. They will definitely be most likely to lean a certain way, but we should leave the open the possiblity that they may still discover a field they haven't considered yet.

The second part of the data was much easier to obtain as I simply wanted to give the user an idea of the income and employment rates of a selection of popular majors. I utilized the job/income data courtesy that FiveThirtyEight used in their article about the earning potential of majors ([here](http://fivethirtyeight.com/features/the-economic-guide-to-picking-a-college-major/)) which can be found [here](https://github.com/fivethirtyeight/data/tree/master/college-majors). The data was originally found via the American Community Survey (ACS) from 2010-2012. I attempted to find more current data, but unfortunately the ACS appears to have removed the major variable from their surveys or I simply am not good enough at navigating their data portal to find it.

<br>
## The Modeling

<br>
## The Product

<br>

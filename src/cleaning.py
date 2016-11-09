import copy
import operator

def majors_string_to_list(qa_lst):
    """
    Converts the string containing the majors associated with each question
    to a list. Returns the modified list.

    Parameters
    ----------
    q_a_lst: list
        List of questions and answers pulled from Loyola website

    Returns
    -------
    cleaned_lst: list
        Copy of qa_lst, list of lists with len 35. Each question is stored in a
        single list and each question list has the question (str) at index 0
        and the majors associated (list) at index 1. See example below:

        [[question1(type: str), majors1_lst(type:list)], ...,
                                [question35(type:str), majors35_lst(type:list)]
    """
    cleaned_lst = copy.deepcopy(qa_lst)

    for question in cleaned_lst:
        question[1] = question[1].split(',')

    return cleaned_lst


def map_to_field(clean_qa):
    """
    Returns qa_lst with added field of study mapping. Maps the collection of
    majors asscociated with each question to a field of study for prediction.

    Parameters
    ----------
    clean_qa: list
        Cleaned list of questions and answers from Loyola website

    Returns
    -------
    mapped_lst: list
        Copy of qa_lst, list of lists with len 35. Adds a third element
        (index 2)to each list which is the field of study mapped to the majors.
        See example below:

        [[question1(type: str), majors1_lst(type:list), field1(type:str)], ...
        ,[question35(type:str), majors35_lst(type:list), field35(type:str)]]

    """
    mapped_lst = copy.deepcopy(clean_qa)
    return None

def all_majors(clean_qa):
    """
    Returns a set of all possible majors from Loyola quiz.

    Parameters
    ----------
    clean_qa: list
        Cleaned list of questions and answers from Loyola website

    Returns
    -------
    majors_set: set
        Set of all possible majors. Majors are strings
    """
    majors_collection = []

    for qa in clean_qa:
        major_lst = qa[1]
        majors_collection.append(major_lst)

    return set(reduce(operator.concat, majors_collection))


def get_fields_dict():
    majors_dict = {
         "Creative Arts": set(['Art History', 'Dance', 'Film and Digital Media',
         'Music', 'Studio Art', 'Theatre', 'Visual Communication']),

         "Math, Sciences, and Engineering": set(['Biochemistry',
         'Bioinformatics', 'Biology', 'Biophysics', 'Chemistry',
         'Communications Networks and Security', 'Economics',
         'Engineering Science', 'Environmental Science',
         'Environmental Studies', 'Exercise Science', 'Information Technology',
         'Mathematics and Computer Science', 'Physics', 'PreHealth',
         'Software Engineering', 'Statistics',
         'Theoretical Physics and Applied Mathematics', 'Computer Science']),

         "Business and Communication": set(['Accounting',
         'Advertising and Public Relations', 'Communication Studies',
         'Education', 'English', 'Entrepreneurship', 'Finance',
         'Human Resources Mgmt','Information Systems',
         'International Business', 'Journalism', 'Marketing',
         'Operations Management','Sports Management']),

         "Social Sciences": set(['African Studies and the African Diaspora',
         'Anthropology', 'Classical Civilization', 'French', 'Greek',
         'History', 'Italian', 'International Studies', 'Latin', 'Philosophy',
         'Psychology', 'Religious Studies', 'Sociology',
         'Sociology and Anthropology', 'Spanish', 'Theology',
         'Womens Studies and Gender Studies']),

         "Public Service, Law, and Policy": set(
         ['Criminal Justice and Criminology', 'Environmental Policy',
         'Forensic Science', 'Health Systems Management', 'Human Services',
         'Nursing', 'Political Science', 'PreLaw', 'Social Work'])
    }
    return majors_dict

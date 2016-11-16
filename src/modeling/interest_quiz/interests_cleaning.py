from __future__ import division
from collections import Counter
import numpy as np
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


def make_counter(question, i, fields_dict):
    """
    Returns a counter dictionary with field_of_study(str):count(int) key-value
    pairs. The count is the number of times that the field_of_study appeared
    in the list of majors associated with the question.

    Takes a list, the index of the list where the list of majors is stored,
    and the dictionary where the mapping of fields to majors is found.

    Parameters
    ----------
    question: list
        A list containing the question and a list of majors associated with
        a positive answer to that question.

    i: int
        The index where the list of majors is stored.

    fields_dict: dictionary
        field_of_study(type: str):majors(type: set) key-value pairs

    Returns
    -------
    Counter: counter dictionary
        field_of_study(str):count(int) key-value pairs.
    """
    fields = []
    for major in question[i]:
        for field, majors_set in fields_dict.iteritems():
            if major in majors_set:
                fields.append(field)
            else:
                continue
    return Counter(fields)


def create_labels(clean_qa, fields_dict):
    """
    Returns qa_lst with added class labels with weights.

    Each question is assigned a primary label with associated weight and a
    secondary label with associated weight. Questions with no secondary label
    have a None type for the secondary label. Each label tuple has
    the format (class_label(type: str), weight(type:float)).

    Parameters
    ----------
    clean_qa: list
        Cleaned list of questions and answers from Loyola website

    Returns
    -------
    mapped_lst: list
        Copy of qa_lst, list of lists with len 35.

        See example below:

        [[question1(type: str), majors1_lst(type:list),
                               label1(type:tup), label2(type:tup)], ...
        ,[question35(type:str), majors35_lst(type:list), field35(type:str)],
                               label1(type:tup), label2(type:tup)]

    """
    mapped_lst = copy.deepcopy(clean_qa)

    for question in mapped_lst:
        cnter = make_counter(question, 1, fields_dict)
        question.append(cnter)

    return mapped_lst


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
    """
    Returns a dictionary with field:majors key-value pairs. Field is a string
    representing a general field of study. Majors is a set containing the
    majors asscociated with the field.

    Fields/keys are as follows:
        "Creative Arts"
        "Math, Sciences, and Engineering"
        "Business and Communication"
        "Social Sciences"
        "Public Service, Law, and Policy"

    Parameters
    ----------
    None

    Returns
    -------
    fields_dict: dictionary,
        field_of_study(type: str):majors(type: set) key-value pairs

    """
    fields_dict = {
         "Creative Arts": set(
                              ['Art History', 'Dance',
                               'Film and Digital Media',
                               'Music', 'Studio Art', 'Theatre',
                               'Visual Communication']),

         "Math, Sciences, and Engineering": set(
                                                ['Biochemistry',
                                                 'Bioinformatics',
                                                 'Biology', 'Biophysics',
                                                 'Chemistry',
                                                 'Communications Networks and Security',
                                                 'Economics',
                                                 'Engineering Science',
                                                 'Environmental Science',
                                                 'Environmental Studies',
                                                 'Exercise Science',
                                                 'Information Technology',
                                                 'Mathematics and Computer Science',
                                                 'Physics', 'PreHealth',
                                                 'Software Engineering',
                                                 'Statistics',
                                                 'Theoretical Physics and Applied Mathematics',
                                                 'Computer Science']),

         "Business and Communication": set(
                                           ['Accounting',
                                            'Advertising and Public Relations',
                                            'Communication Studies',
                                            'Education', 'English',
                                            'Entrepreneurship', 'Finance',
                                            'Human Resources Mgmt',
                                            'Information Systems',
                                            'International Business',
                                            'Journalism', 'Marketing',
                                            'Operations Management',
                                            'Sports Management']),

         "Social Sciences": set(
                                ['African Studies and the African Diaspora',
                                 'Anthropology', 'Classical Civilization',
                                 'French', 'Greek', 'History', 'Italian',
                                 'International Studies', 'Latin',
                                 'Philosophy', 'Psychology',
                                 'Religious Studies', 'Sociology',
                                 'Sociology and Anthropology', 'Spanish',
                                 'Theology',
                                 'Womens Studies and Gender Studies']),

         "Public Service, Law, and Policy": set(
                                                ['Criminal Justice and Criminology',
                                                 'Environmental Policy',
                                                 'Forensic Science',
                                                 'Health Systems Management',
                                                 'Human Services', 'Nursing',
                                                 'Political Science', 'PreLaw',
                                                 'Social Work'])
    }
    return fields_dict

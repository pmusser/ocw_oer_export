"""
Module for creating OER-template CSV file with data extracted from MIT OpenCourseWare API.
"""

import csv
import os
import logging


from .client import extract_data_from_api
from .data_handler import extract_data_from_json
from .config import API_URL
from .utilities import normalize_course_url, normalize_keywords, text_cleanup


def create_fm_ocw_course_url_to_keywords_mapping(path=None, file_name=None):
    """
    Creates a mapping from OCW course URLs to their associated keywords using FM export data.

    This function reads a CSV file and extracts the mapping between course URLs and their keywords.
    """
    if path is None:
        path = os.path.dirname(__file__)

    if file_name is None:
        file_name = "mapping_files/fm_keywords_export.csv"

    file_path = os.path.join(path, file_name)
    course_map = {}

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["zze_courseURL"]:
                course_url = normalize_course_url(row["zze_courseURL"])
                course_map[course_url] = row["zzd_keywords"]
    return course_map


def create_ocw_topic_to_oer_subject_mapping(path=None, file_name=None):
    """
    Create a mapping from OCW (OpenCourseWare) topics to OER (Open Educational Resources) subjects.

    This function reads a CSV file containing mappings specified by the arguments.
    It creates a dictionary where keys are OCW topics and values are the corresponding OER subjects.
    The function does not perform any manipulation on the mapping data.
    """
    if path is None:
        path = os.path.dirname(__file__)

    if file_name is None:
        file_name = "mapping_files/ocw_topic_to_oer_subject.csv"

    file_path = os.path.join(path, file_name)
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return {row["OCW Topic"]: row["OER Subject"] for row in reader}


def get_cr_sublevel(levels):
    """Set the value(s) of CR_SUBLEVEL based on the course levels."""
    level_mappings = {
        "Undergraduate": ["Community College/Lower Division", "College/Upper Division"],
        "Graduate": ["Graduate/Professional"],
        "High School": ["High School", "Community College/Lower Division"],
        "Non-Credit": ["Career/Technical Education"],
    }
    sublevels = [
        sublevel for level in levels for sublevel in level_mappings.get(level["name"])
    ]
    return "|".join(sorted(set(sublevels)))


def get_description_in_plain_text(description):
    """Get Course Resource plain text description by cleaning up markdown and HTML."""
    cleaned_description = text_cleanup(description)
    return cleaned_description


def get_cr_subjects(ocw_topics_mapping, ocw_course_topics):
    """
    Get OER formatted Course Resource Subjects list.

    Since distinct OCW topics can map to the same OER subject, duplicate subject
    values are omitted.
    """
    oer_subjects_list = [
        ocw_topics_mapping.get(topic["name"]).split("|")
        if ocw_topics_mapping.get(topic["name"]) is not None
        else []
        for topic in ocw_course_topics
    ]
    unique_oer_subjects = set(
        subject for subjects in oer_subjects_list for subject in subjects
    )
    sorted_unique_oer_subjects = sorted(unique_oer_subjects)
    return "|".join(sorted_unique_oer_subjects)


def get_cr_keywords(fm_ocw_keywords_mapping, list_of_topics_objs, course_url):
    """
    Get OER formatted Course Resource keywords for a given OCW course.

    It checks for course's keywords in FM export mapping (fm_ocw_keywords_mapping).
    If no keywords are found there, it uses OCW course's topics as keywords.
    """
    keywords = fm_ocw_keywords_mapping.get(course_url)
    if keywords:
        return normalize_keywords(keywords)
    return "|".join(topic["name"] for topic in list_of_topics_objs)


def get_cr_create_date(semester, year):
    """Convert a semester and year into a ballpark start date."""
    semester_start_dates = {
        "Fall": "09-01",
        "Spring": "02-01",
        "Summer": "06-01",
        "January IAP": "01-01",
    }
    start_date = semester_start_dates.get(semester)
    if start_date and year:
        return f"{year}-{start_date}"
    if year:
        return f"{year}-01-01"
    return ""


def get_cr_authors(list_of_authors_objs):
    """Get OER formatted Course Resource Authors list."""
    return "|".join(
        f"{author['last_name']}, {author['first_name']}"
        for author in list_of_authors_objs
    )


def get_cr_educational_use(ocw_course_feature_tags):
    """
    Get OER formatted Course Resource Educational Uses list based on OCW Course Feature tags.

    This function analyzes the feature tags of a course and includes:
    - 'Curriculum', and 'Instruction' for every course
    - 'Assessment' if the feature tags include 'Assignment'.
    - 'Professional Development' if the feature tags include 'Instructor Insights'.
    """
    tags = ["Curriculum/Instruction"]
    assessment_flag = any("Assignment" in tag for tag in ocw_course_feature_tags)
    professional_dev_flag = "Instructor Insights" in ocw_course_feature_tags

    if assessment_flag:
        tags.append("Assessment")

    if professional_dev_flag:
        tags.append("Professional Development")

    return "|".join(tags)


def get_cr_accessibility(ocw_course_feature_tags):
    """
    Get OER formatted Course Resource Accessibility tags list based on OCW Course Feature tags.

    This function analyzes the feature tags of a course and includes:
    - 'Visual', and 'Textual' for every course
    - 'Auditory', 'Caption', and 'Transcript'  if the feature tags include 'Video'.
    """
    tags = ["Visual|Textual"]
    video_flag = any("Video" in tag for tag in ocw_course_feature_tags)

    if video_flag:
        tags.append("Auditory|Caption|Transcript")

    return "|".join(tags)


def transform_single_course(course, ocw_topics_mapping, fm_ocw_keywords_mapping):
    """Transform a single course according to OER template."""
    course_runs = course["runs"][0]
    return {
        "CR_TITLE": course["title"],
        "CR_URL": course_runs["url"],
        "CR_MATERIAL_TYPE": "Full Course",
        "CR_MEDIA_FORMATS": "Text/HTML",
        "CR_SUBLEVEL": get_cr_sublevel(course_runs["level"]),
        "CR_ABSTRACT": get_description_in_plain_text(course_runs["description"]),
        "CR_LANGUAGE": "en",
        "CR_COU_TITLE": "Creative Commons Attribution Non Commercial Share Alike 4.0",
        "CR_PRIMARY_USER": "student|teacher",
        "CR_SUBJECT": get_cr_subjects(ocw_topics_mapping, course["topics"]),
        "CR_KEYWORDS": get_cr_keywords(
            fm_ocw_keywords_mapping, course["topics"], course_runs["url"]
        ),
        "CR_CREATE_DATE": get_cr_create_date(
            course_runs["semester"], course_runs["year"]
        ),
        "CR_AUTHOR_NAME": get_cr_authors(course_runs["instructors"]),
        "CR_PROVIDER": "MIT",
        "CR_PROVIDER_SET": "MIT OpenCourseWare",
        "CR_COU_URL": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "CR_COU_COPYRIGHT_HOLDER": get_cr_authors(course_runs["instructors"]),
        "CR_EDUCATIONAL_USE": get_cr_educational_use(course["course_feature"]),
        "CR_ACCESSIBILITY": get_cr_accessibility(course["course_feature"]),
    }


def transform_data(data):
    """Transform all courses into OER template."""
    fm_ocw_keywords_mapping = create_fm_ocw_course_url_to_keywords_mapping()
    ocw_topics_mapping = create_ocw_topic_to_oer_subject_mapping()

    return [
        course
        for course in (
            transform_single_course(course, ocw_topics_mapping, fm_ocw_keywords_mapping)
            for course in data
        )
        if course is not None
    ]


def create_csv(
    source="api",
    input_path="/private/output/ocw_api_data.json",
    output_path="/private/output/ocw_oer_export.csv",
):
    """
    Create a CSV file from either the MIT OpenCourseWare API or a locally stored JSON file.
    output_path: The output path inside the docker container.
    """
    api_data_json = {}

    if source == "api":
        api_data_json = extract_data_from_api(api_url=API_URL)

    elif source == "json":
        api_data_json = extract_data_from_json(input_path)

    else:
        raise ValueError("Invalid source. Use 'api' or 'json'.")

    transformed_data = transform_data(api_data_json)
    fieldnames = [
        "CR_TITLE",
        "CR_URL",
        "CR_MATERIAL_TYPE",
        "CR_MEDIA_FORMATS",
        "CR_SUBLEVEL",
        "CR_ABSTRACT",
        "CR_LANGUAGE",
        "CR_COU_TITLE",
        "CR_PRIMARY_USER",
        "CR_SUBJECT",
        "CR_KEYWORDS",
        "CR_CREATE_DATE",
        "CR_AUTHOR_NAME",
        "CR_PROVIDER",
        "CR_PROVIDER_SET",
        "CR_COU_URL",
        "CR_COU_COPYRIGHT_HOLDER",
        "CR_EDUCATIONAL_USE",
        "CR_ACCESSIBILITY",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed_data)
        logging.info(
            "CSV file '%s' successfully created.",
            output_path,
        )

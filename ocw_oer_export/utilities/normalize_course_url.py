"""
Module for normalizing OCW FM export course URLs to the format comparable with MIT Learn's API.
"""


def normalize_course_url(url):
    """
    The OCW FM export format includes the department name:
    'ocw.mit.edu/courses/department_name/course_metadata'

    This function removes the 'department_name' to match the MIT Learn's API format:
    'ocw.mit.edu/courses/course_metadata'

    Example:
    Input: 'ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010'
    Output: 'ocw.mit.edu/courses/18-06-linear-algebra-spring-2010'
    """
    if "/courses/" in url:
        base_url, course_path = url.split("/courses/", 1)
        course_metadata = course_path.split("/", 1)[1]
        normalized_url = base_url + "/courses/" + course_metadata
        return normalized_url
    return url

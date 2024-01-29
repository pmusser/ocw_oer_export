"""
Module for normalizing OCW FM export course keywords.
"""

import re
from titlecase import titlecase


def normalize_keywords(keywords):
    """
    Normalizes keywords from the OCW FM export file to a standardized, pipe-separated format.

    The OCW FM export file may contain keywords in various formats, including comma-separated,
    semicolon-separated, newline-separated, double newlines separated, or multiples of these.

    This function converts these formats into a standardized format used in OER: a pipe-separated
    string where each keyword's first letter is capitalized.

    Example:
    Input:  "novel, short story, the city in literature,narrative voice"
    Input:  "novel\n\nshort story\n\nthe city in literature\n\nnarrative voice"
    Output: "Novel|Short Story|The City In Literature|Narrative Voice"
    """
    normalized_keywords = re.sub(r"[;,]|\n\n|\n", "|", keywords).strip()
    keywords_list = [
        titlecase(keyword) if not keyword.isupper() else keyword
        for keyword in (
            normalized_keyword.strip()
            for normalized_keyword in normalized_keywords.split("|")
        )
        if keyword
    ]
    return "|".join(keywords_list)

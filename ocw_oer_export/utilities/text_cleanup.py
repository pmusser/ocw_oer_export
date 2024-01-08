"""
Module for cleaning up HTML and Markdown mixed text coming out of MIT's OCW Studio's CKEditor.
"""

import re
from io import StringIO
from markdown import Markdown


def cleanup_curly_brackets(text):
    """
    Remove content within curly brackets, including the brackets themselves, from the input string.
    Also remove any lines that become empty as a result of this removal.
    """
    pattern = re.compile(r"\{\{.*?\}\}\n?")
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def html_to_text(html):
    """Remove HTML tags from an HTML string."""
    pattern = re.compile("<.*?>")
    return re.sub(pattern, "", html)


def create_markdown_converter():
    """Create and configure a Markdown converter for plain text output."""

    def unmark_element(element, stream=None):
        """Helper function to recursively extract text from Markdown elements."""
        if stream is None:
            stream = StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()

    # patching Markdown
    Markdown.output_formats["plain"] = unmark_element
    markdown_converter = Markdown(output_format="plain")
    markdown_converter.stripTopLevelTags = False
    return markdown_converter


def markdown_to_text(markdown):
    """Convert Markdown to plain text using the markdown_converter."""
    markdown_converter = create_markdown_converter()
    return markdown_converter.convert(markdown)


def text_cleanup(text):
    """
    Perform text cleanup by:
    1. Converting Markdown to text,
    2. Removing HTML tags,
    3. Cleaning up curly brackets.
    """
    stripped_markdown = markdown_to_text(text)
    stripped_html = html_to_text(stripped_markdown)
    cleaned_text = cleanup_curly_brackets(stripped_html)
    return cleaned_text

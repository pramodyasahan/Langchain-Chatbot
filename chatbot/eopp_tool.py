from langchain.tools import tool


@tool("match_eopp")
def match_eopp(
    name: str,
    date_of_birth: str,
    address: str,
    contact_number: str,
    email_id: str,
    latest_qualification: str,
    qualification_info: dict = None
) -> str:
    """
    Matches EOPPs based on user details and qualification info.

    - latest_qualification (str): One of 'O-levels', 'A-Level', 'Bachelors', 'Masters'.
    - qualification_info (dict): Dict with extra details based on qualification:
        if 'O-levels': {'english_result': str, 'maths_result': str, 'science_result': str}
        if 'A-Level': {'a_level_results': str} (example: ACB)
        if 'Bachelors': {'stream_of_study_bachelors': str, 'gpa_bachelors': float, 'bring_dependents_bachelors': str (Y/N)}
        if 'Masters': {'stream_of_study_masters': str, 'gpa_masters': float, 'bring_dependents_masters': str (Y/N)}

    Example:
        "John Doe", "1990-01-01", "123 Main St", "+1234567890", "john@example.com", "A-Level", {"a_level_results": "CCC"}
    """  # noqa: E501

    if qualification_info is None:
        return "Missing qualification_info. Please provide details based on your latest qualification."

    # logic here
    # return "success"
    return (
        "Thank you for providing your details! I've started the process of finding "
        "the best educational opportunities for you. You will receive an email once the matching process is completed. "
        "Feel free to reach out if you have any questions in the meantime!"
    )

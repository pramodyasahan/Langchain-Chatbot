import json

from langchain.tools import tool

from chatbot.filter import initial_filtering


@tool()
def initial_filtering_tool(filters_json: str) -> str:
    """
    Initial Filtering Tool:

    Filters courses based on key criteria provided in a JSON string. For example,
    to retrieve all Bachelor's degree courses, you can pass:

        {
            "university name": null,
            "field type": "engineering",
            "location": "london",
            "degree program type": "bachelor's"
        }

    The tool returns a comma-separated list of course names that match the criteria,
    or a message indicating no courses were found.
    """
    try:
        filters = json.loads(filters_json)
    except Exception as e:
        return f"Error parsing filters JSON: {e}"

    file_path = "chatbot/data/processed/updated_data.xlsx"  # Update this path as needed
    filtered_df = initial_filtering(file_path, filters)

    if filtered_df.empty:
        return "No courses found matching the provided criteria."

    courses_and_universities = [
        f"{row['university_name']} - {row['course_or_degree_name']}" 
        for _, row in filtered_df.iterrows()
    ]
    
    # Join the results into a comma-separated string
    return ", ".join(courses_and_universities)

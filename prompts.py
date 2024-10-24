def get_short_jd_prompt():
    return """
    A job description will be given in the next prompt. Make it clear and concise. 
    Keep required, desired, preferred skills and certifications.
    Should not exceed more than 15 lines.
    Don't use any embedding while generating response, eg: bold, italic.
    use the below format
    """


def get_change_tense_prompt():
    return """Convert all listed responsibilities to past tense. Do not make any other changes."""

def get_analyse_prompt():
    return """
    Check the Candidate is genuine.
    Check responsibilities relevant to job title.
    Check for inconsistencies in location and timeline, particularly regarding education and employment.
    give clear and concise response in bullet points. don't give recommendations.
    """


def get_skill_matrix_prompt():
    return f"""
    A list of skills will be provided wait for the prompt.
    Calculate the candidate's years of experience for each skill using only the employment history section of the resume.
    If no experience is found, return 'NA'.
    Ignore the profile summary and technical skills sections.
    Provide only the years, no explanations."""


def get_format_to_nc_prompt(resume_content):
    return f"""
    Please format the following resume content to NC style, while formatting follow the rules below:
     1. The Government Experience section aims to glimpse the candidate's relevant government experience.
     2. In the Employment History section, candidates' full experience should be listed in descending chronological order. Including government experience.
     3. You can rearrange the resume but do not add, remove, or modify any text content. Don't try to correct grammar erorrs, even if you find any. Don't inculde profile summary and technical skills sections.
     4. Give one line space before each employment.
     5. IMPORTANT: Don't remove any text content from employment history. if it doesn't fit the NC Style leave it as it is.
     6. Don't use any embedding while generating response, eg: bold, italic.

    {resume_content}

    NC Style:
    <Candidate Name>
    GOVERNMENT EXPERIENCE (Don't add responsibilities here)
    •	Client Name, City, State	Mon (first three alphabets) YYYY – Mon (first three alphabets) YYYY

    CERTIFICATIONS
    List all certificates here

    Employment History
    Client Name, City, State	Mon (first three alphabets) YYYY – Mon (first three alphabets) YYYY
    Job Title
    Responsibilities(heading)
    •	Responsibility 1
    •	Responsibility 2
    ....

    Education
    •	Degree – University, City, State, passed out year
    """

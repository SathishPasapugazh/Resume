def get_short_jd_prompt():
    return """
    A job description will be given in the next prompt (You should respond "I'm waiting"). Deeply analyse the jd and answer the below questions. 
    1. What client wants (bullet points)
    2. What skills candidate need (bullet points)
    3. What is candidate going to do (bullet points)
    4. Short Boolean string (include job title with necessary skills)
    
    keep the response clear and concise. Use simple English. Don't use any embedding like bold, italic.
    """


def get_change_tense_prompt():
    return """Convert all listed responsibilities to past tense. Do not make any other changes."""

def get_analyse_prompt():
    return """
Analyze the candidate's resume based on the following criteria: 
1. Check whether the listed responsibilities are relevant to the job title.
2. Check for inconsistencies in location and timeline, particularly regarding education and employment. 
3. Check for gaps in employment history. if the previous project ended and next project starts in the same month its not a problem.
4. Check for evidence of falsification.
    """


def get_skill_matrix_prompt():
    return f"""
    A list of skills will be provided wait for the prompt.
    Calculate the candidate's years of experience for each skill using only the employment history section of the resume. Ignore the profile summary and technical skills sections.
    If no experience is found, return 'NA'. If skills related to certification response with 'Yes' or 'No'.
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

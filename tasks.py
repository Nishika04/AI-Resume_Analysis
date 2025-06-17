# Tasks - Find the Job Requirements, Resume Swot Analysis
from crewai import Task
from agents import agents
# from salary_benchmark import salary_benchmark_agent

def tasks(llm, job_desire, resume_short):
    '''
    job_requirements_research - Find the relevant skills, projects and experience
    resume_swot_analysis- understand the report and the resume based on this make a swot analysis
    '''

    job_requirements_researcher, resume_swot_analyser, course_researcher, job_role_recommender, skill_gap_identifier, ats_optimization_advisor, cover_letter_generator, career_trajectory_depicter,  mock_interview_generator, networking_opportunities_agent, elevator_pitch_generator= agents(llm)

    research = Task(

        description=f'For Job Position of Desire: {job_desire} research to identify the current market requirements for a person at the job including the relevant skills, some unique research projects or common projects along with what experience would be required. For searching query use ACTION INPUT KEY as "search_query"',
        expected_output='A report on what are the skills required and some unique real time projects that can be there which enhances the chance of a person to get a job',
        agent=job_requirements_researcher
    )
    

    resume_swot_analysis = Task(

        description=f'Resume Content: {resume_short} \n Analyse the resume provided and the report of job_requirements_researcher to provide a detailed SWOT analysis report on the resume along with the Resume Match Percentage and Suggestions to improve',
        expected_output='A PURE JSON formatted report without any preceding text or labels as follows: "candidate": candidate, "strengths":[strengths], "weaknesses":[weaknesses], "opportunities":[opportunities], "threats":[threats], "resume_match_percentage": resume_match_percentage, "suggestions": "suggestions"',
        agent=resume_swot_analyser,
        output_file='resume-report/resume_review.json'
    )

    courses = Task(

    description=f'For Job Position of Desire: {job_desire}, research and provide a list of the most relevant courses and project ideas that will help the user upskill and become more suitable for the role.',
    expected_output='A plain JSON formatted report without any preceding text or labels as follows: "domain": job_desire, "courses": [{"title": title, "platform": platform, "outcome": outcome, "link": link}], "recommended_projects": [project_ideas]',
    agent=course_researcher,
    output_file='resume-report/courses.json'
    )

    job_roles = Task(
        description=f'Resume Content: {resume_short} \n Based on the candidate\'s profile, recommend a list of job roles they are best suited for. '
                    f'Take into consideration their technical and soft skills, experience, and overall profile.',
        expected_output='A PURE JSON formatted list without any preceding text or labels like: {"recommended_roles": ["Data Analyst", "NLP Engineer", "ML Engineer"]}',
        agent=job_role_recommender,
        output_file='resume-report/job_roles.json'
    )

    skill_gap_analysis = Task(
        description=f'Resume Content: {resume_short} \n Compare the resume with the current job requirements for the role of {job_desire}. '
                    f'Identify the skills missing in the resume compared to the job requirements and return them.',
        expected_output='A pure JSON list without any preceding text or labels of missing skills: {"missing_skills": ["Skill1", "Skill2", "Skill3"]}',
        agent=skill_gap_identifier,
        output_file='resume-report/skill_gap.json'
    )

    ats_optimization = Task(
        description=f'Resume Content: {resume_short} \n Analyze the resume and suggest changes to make it more ATS-friendly. '
                    f'Ensure the resume is properly formatted, with relevant keywords and sections to improve chances of passing through ATS filters.',
        expected_output='Return your response as a JSON object in detail, with a few examples in the format:{"suggestions": ["Add relevant skills", "Use action verbs", "Properly format headings"]}',
        agent=ats_optimization_advisor,
        output_file='resume-report/ats_optimization.json'
    )

    cover_letter_task = Task(
        description=f'Resume Content: {resume_short} \n Desired Job Role: {job_desire} \n Generate a personalized, professional cover letter addressing the candidate’s skills, achievements, and alignment to the desired role.',
        expected_output='A professional cover letter text formatted in paragraphs suitable for direct use in applications.',
        agent=cover_letter_generator,
        output_file='resume-report/cover_letter.txt'
    )

    career_trajectory_task = Task(
        description=f'Resume Content: {resume_short} \n Analyze the candidate’s work experience, if any, and depict their career trajectory and growth over time. '
                    f'If no experience is found, suggest gaining experience through internships, certifications, volunteering, or personal projects.',
        expected_output='A pure JSON formatted output without any preceding text or labels: {"career_summary": "text", "career_path": [{"year": "year", "title": "title"}], "suggestions_if_no_experience": ["suggestion1", "suggestion2"]}',
        agent=career_trajectory_depicter,
        output_file='resume-report/career_trajectory.json'
    )

    mock_interview = Task(
        description=f"Based on the resume content: {resume_short} and the desired job role: {job_desire}, generate a mock interview with 5-7 personalized questions. Also provide ideal sample answers based on the resume context.",
        expected_output='A pure JSON formatted output without any preceding text or labels: {"questions": [{"question": "...", "ideal_answer": "..."}]}',
        agent=mock_interview_generator,
        output_file="resume-report/mock_interview.json"
    )

    networking_task = Task(
        description=f"Given the candidate's resume and the target job role of '{job_desire}', recommend networking opportunities to grow professionally. Include LinkedIn groups, relevant conferences, active communities (Reddit, Discord, Slack), and key people to follow.",
        expected_output='''
        A pure JSON formatted output without any preceding text or labels:
        {
          "job_role": "string",
          "linkedin_groups": [list of group names and brief reasons],
          "online_communities": [list of community names/platforms],
          "conferences": [list of top events],
          "influencers_to_follow": [list of people with platform & why to follow]
        }
        ''',
        agent=networking_opportunities_agent,
        output_file='resume-report/networking_opportunities.json'
    )

    elevator_pitch_task = Task(
        description=(
            f"Based on the resume and the user's desired job as a {job_desire}, write a compelling 30-second elevator pitch. "
            f"Keep it concise and tailored to highlight their key achievements, skills, and aspirations."
        ),
        expected_output='''
        A pure JSON formatted output without any preceding text or labels:
        {
          "job_role": "string",
          "elevator pitch": "string"
        }
        ''',
        output_file='resume-report/elevator_pitch.txt',
        agent=elevator_pitch_generator,
        async_execution=False
    )

#     job_fit_score_task = Task(
#     description={
#         "resume": resume_short,
#         "job_description": job_description,
#         "summary": "Provide a 'Job Fit Score' between 0 and 100 based on skill, experience, and keyword relevance."
#     },
#     expected_output={
#         "score": "Number between 0 and 100",
#         "skill_match": "Percentage of skills matched",
#         "experience_match": "Percentage of experience matched",
#         "keyword_overlap": "Percentage of keyword overlap",
#         "summary": "Summary of the fit score"
#     },
#     agent=job_fit_score_agent,
#     output_file="resume-report/job_fit_score.json"
# )



    return research, resume_swot_analysis, courses, job_roles, skill_gap_analysis, ats_optimization, cover_letter_task, career_trajectory_task, mock_interview, networking_task, elevator_pitch_task

    # return {
    #     "research": research, 
    #     "resume_swot_analysis": resume_swot_analysis,
    #     "courses": courses,
    #     "job_roles": job_roles,
    #     "skill_gap_analysis": skill_gap_analysis,
    #     "ats_optimization": ats_optimization,
    #     "cover_letter_task": cover_letter_task,
    #     "career_trajectory_task": career_trajectory_task,
    #     "mock_interview": mock_interview
    #     # "networking_task": networking_task
    # }

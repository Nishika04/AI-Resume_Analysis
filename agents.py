# Agents
# 1. Job Requirements Researcher
# 2. SWOT Analyser

## Importing the dependencies

from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool

search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# Create agents which uses these tools

def agents(llm):
    '''
    Has two agents
    1. requirements_researcher - search_tool, web_rag_tool
    2. swot_analyser
    '''
    job_requirements_researcher = Agent(
                                            role='Market Research Analyst',
                                            goal='Provide up-to-date market analysis of industry job requirements of the domain specified',
                                            backstory='An expert analyst with a keen eye for market trends.',
                                            tools=[search_tool, web_rag_tool],
                                            verbose=True,
                                            llm=llm,
                                            max_iters=1
                                        )
    
    resume_swot_analyser = Agent(
                                    role='Resume SWOT Analyser',
                                    goal=f'Perform a SWOT Analysis on the Resume based on the industry Job Requirements report from job_requirements_researcher and provide a json report.',
                                    backstory='An expert in hiring so has a great idea on resumes',
                                    verbose=True,
                                    llm=llm,
                                    max_iters=1,
                                    allow_delegation=True
                            )

    course_researcher = Agent(
        role='Course Recommendation Specialist',
        goal='Suggest the most relevant courses for a job role',
        backstory="You're a learning and development expert who identifies valuable certifications and courses.",
        llm=llm
    )

    job_role_recommender = Agent(
        role="Job Role Recommender",
        goal="Recommend the best-fit job roles based on resume content and career interests",
        backstory="A career coach AI trained on thousands of job descriptions and resumes to guide users toward fitting roles.",
        llm=llm
    )

    
    skill_gap_identifier = Agent(
        role="Skill Gap Identifier",
        goal="Identify the skill gaps in the candidate’s profile compared to the job requirements.",
        backstory="An expert in identifying missing skills that prevent candidates from qualifying for specific roles.",
        llm=llm
    )

    
    ats_optimization_advisor = Agent(
        role="ATS Optimization Advisor",
        goal="Suggest improvements to optimize the resume for better performance in Applicant Tracking Systems.",
        backstory="An expert in crafting resumes optimized for ATS by ensuring the right keywords, structure, and format.",
        llm=llm
    )

    cover_letter_generator = Agent(
        role="Cover Letter Generator",
        goal="Generate a professional and personalized cover letter tailored to the candidate’s resume and desired job role.",
        backstory="An experienced HR consultant skilled at writing compelling cover letters that highlight the candidate’s strengths and align them with the target job.",
        llm=llm
    )
    
    career_trajectory_depicter = Agent(
        role="Career Trajectory Depicter",
        goal="Analyze the candidate’s resume and depict their career growth over time. If no professional experience is found, suggest gaining experience through internships, certifications, or projects.",
        backstory="An experienced career counselor with a knack for identifying professional growth paths and providing guidance when experience is missing.",
        llm=llm
    )

    mock_interview_generator = Agent(
            role="Expert Interview Coach",
            goal="Generate mock interview questions and ideal answers tailored to the user's resume and desired job role",
            backstory="You're an experienced HR professional and technical interviewer who prepares job candidates with personalized mock interviews.",
            verbose=True,
            llm=llm
    )

    networking_opportunities_agent = Agent(
            role='Networking Advisor',
            goal='Recommend networking opportunities, events, and platforms for the candidate to grow in their desired domain.',
            backstory='You are an expert in identifying communities, events, and industry influencers that job seekers should engage with to grow their network.',
            llm=llm
    )

    elevator_pitch_generator = Agent(
        role='Elevator Pitch Generator',
        goal='Craft a concise, persuasive, and impactful 30-second pitch highlighting the candidate’s strengths, experience, and aspirations.',
        backstory=(
            "You are an expert career strategist who helps professionals make powerful first impressions. "
            "You know how to distill complex achievements into simple, memorable statements."
        ),
        verbose=True,
        llm=llm
    )


    return job_requirements_researcher, resume_swot_analyser, course_researcher, job_role_recommender, skill_gap_identifier, ats_optimization_advisor, cover_letter_generator, career_trajectory_depicter, mock_interview_generator, networking_opportunities_agent, elevator_pitch_generator



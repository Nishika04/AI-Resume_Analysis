# # Importing the dependencies

# import os
# from crewai import Crew, Process
# from dotenv import load_dotenv, find_dotenv
# from langchain_openai import ChatOpenAI 
# from utils import *
# from agents import agents
# from tasks import tasks
# from career_plotter import plot_career_trajectory

# # load_dotenv(find_dotenv())

# # Load environment variables
# load_dotenv(find_dotenv())

# # Configuration (Optional: if you want to use in code directly too)
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Load the LLM using OpenAI
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)

# # Provided the inputs
# resume = read_all_pdf_pages("data\DevangTyagi_resume_one_page.pdf")
# sections = extract_relevant_sections(resume)

# # Generate compact version
# resume_short = generate_short_resume(sections)

# job_desire = input("Enter Desiring Job: ")

# # Creating agents and tasks
# job_requirements_researcher, resume_swot_analyser, course_researcher, job_role_recommender, skill_gap_identifier, ats_optimization_advisor, cover_letter_generator, career_trajectory_depicter, mock_interview_generator, networking_opportunities_agent = agents(llm)
# research, resume_swot_analysis, courses, job_roles, skill_gap_analysis, ats_optimization, cover_letter_task, career_trajectory_task, mock_interview, networking_task = tasks(llm, job_desire, resume_short)

# # Building crew and kicking it off
# crew = Crew(
#     agents=[job_requirements_researcher, resume_swot_analyser, course_researcher, job_role_recommender, skill_gap_identifier, ats_optimization_advisor, cover_letter_generator, career_trajectory_depicter, mock_interview_generator, networking_opportunities_agent],
#     tasks=[research, resume_swot_analysis, courses, job_roles, skill_gap_analysis, ats_optimization, cover_letter_task, career_trajectory_task, mock_interview, networking_task],
#     verbose=1,
#     process=Process.sequential
# )

# result = crew.kickoff()
# print(result)

# # Once the tasks are completed and the JSON is saved:
# plot_career_trajectory('resume-report/career_trajectory.json')






# Importing the dependencies

import os
from crewai import Crew, Process
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI 
from utils import *
from agents import agents
from tasks import tasks
from career_plotter import plot_career_trajectory

# Load environment variables
load_dotenv(find_dotenv())

# Configuration (Optional: if you want to use in code directly too)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Load the LLM using OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)

# Provided the inputs
resume_path = "data\Apratim Pandey Resume.pdf"
resume = read_all_pdf_pages(resume_path)
sections = extract_relevant_sections(resume)
resume_short = generate_short_resume(sections)

job_desire = input("Enter Desiring Job: ")

# Creating agents and tasks
job_requirements_researcher, resume_swot_analyser, course_researcher, job_role_recommender, skill_gap_identifier, ats_optimization_advisor, cover_letter_generator, career_trajectory_depicter, mock_interview_generator, networking_opportunities_agent, elevator_pitch_generator = agents(llm)
research, resume_swot_analysis, courses, job_roles, skill_gap_analysis, ats_optimization, cover_letter_task, career_trajectory_task, mock_interview, networking_task, elevator_pitch_task = tasks(llm, job_desire, resume_short)

# Caching logic
cache_hash = generate_cache_hash(resume_short, job_desire)

all_tasks = [
    research, resume_swot_analysis, courses, job_roles, skill_gap_analysis,
    ats_optimization, cover_letter_task, career_trajectory_task,
    mock_interview, networking_task, elevator_pitch_task
]

task_outputs = [
    'resume-report/skills.json',
    'resume-report/resume_review.json',
    'resume-report/courses.json',
    'resume-report/job_roles.json',
    'resume-report/skill_gap.json',
    'resume-report/ats_optimization.json',
    'resume-report/cover_letter.txt',
    'resume-report/career_trajectory.json',
    'resume-report/mock_interview.json',
    'resume-report/networking_opportunities.json',
    'resume-report/elevator_pitch.txt'
]

# Filter tasks using cache
filtered_tasks = []
for task, output_filename in zip(all_tasks, task_outputs):
    wrapped = load_or_create_task(task, output_filename, cache_hash)
    if wrapped is not None:
        filtered_tasks.append(wrapped)

# Building crew and kicking it off
crew = Crew(
    agents=[
        job_requirements_researcher, resume_swot_analyser, course_researcher,
        job_role_recommender, skill_gap_identifier, ats_optimization_advisor,
        cover_letter_generator, career_trajectory_depicter,
        mock_interview_generator, networking_opportunities_agent, elevator_pitch_generator
    ],
    tasks=filtered_tasks,
    verbose=1,
    process=Process.sequential
)

result = crew.kickoff()
print(result)

# Once the tasks are completed and the JSON is saved:
plot_career_trajectory('resume-report/career_trajectory.json')

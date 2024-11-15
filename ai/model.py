from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from guidance import user, system, assistant,models,gen
import io
import sys

import re


from langchain.agents import initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun
import json


def generate_subTask(user,task):
    name = user['name']
    workLifeRatio = user['workLifeRatio']
    job = user['job']
    gender = user['gender']
    furtherDetails = user['furtherDetails']
    preferTask = user['preferTask'] if len(user['preferTask'])!=0 else "None"
    age = user['age']

    taskTitle = task['title']
    taskBody = task['body']
    startTime = task['start']
    endTime = task['end']
    category = task['category']

    llm = ChatOpenAI(model="gpt-4o-mini")
    
    prompt = f"""You are a task planning assistant. Your role is to generate a main task with subtasks based on the following information:

USER PARAMETERS:
- Name: {name}
- Gender: {gender}
- Work-Life Balance: {workLifeRatio} (consider this ratio when planning task durations)
- Job: {job} (tailor tasks to this professional context)
- Additional Context: {furtherDetails} (incorporate relevant background details)
- User characteristics: {preferTask}
- Age : {age}

TASK PARAMETERS:
- Main Task Title: {taskTitle}
- Task Description: {taskBody}
- Time Window: From {startTime} [to {endTime}]
- Task Category: {category}

Please analyze these parameters and create a structured task plan. The time allocation should respect the user's work-life ratio of {workLifeRatio}, and tasks should be appropriate for someone who is a {job}.

Generate output in this exact format when {endTime} is provided:
"""+"""{
  "title": "Main task title",
  "body": "Main task description",
  "start": [unix_timestamp],
  "end": [unix_timestamp],
  "category": "time",
  "subTasks": [
    {
      "title": "Subtask title",
      "start": [unix_timestamp],
      "end": [unix_timestamp],
      "category": "time"
    }
  ]
}

Generate output in this exact format when {endTime} is NOT provided:
{
  "title": "Main task title",
  "body": "Main task description",
  "start": [unix_timestamp],
  "category": "task",
  "subTasks": [
    {
      "title": "Subtask title",
      "start": [unix_timestamp],
      "category": "task"
    }
  ]
}""" + """

Requirements:
1. subtasks must be specific and actionable
2. timestamps must be valid Unix timestamps within the main task's timeframe
3. category must be "time" if {endTime} is provided, otherwise "task"
4. subtasks should follow a logical sequence
5. timing should account for the user's work-life ratio of {workLifeRatio}
6. tasks should be appropriate for a {job} with background in {furtherDetails}
7. answer to korean
"""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"


##사용법
# """{
# 	"user":{
# 		"name":"김스파르타",
# 		"workLifeRatio":"70:30",
# 		"job": "학생",
# 		"gender": "남자",
# 		"furtherDetails": "ai 교육과정 수강생",
# 		"preferTask":"",
#         "age": "20"
# 	},
# 	"task":{
# 			"title": "AI- 해커톤 ",
# 			"body": "",
# 			"start": 1731651166, 
# 			"end": 1731658366,
# 			"category": "time"
# 	}
# }"""

#user랑 task 데이터를 따로 아래 처럼 넣었습니다.
#result = generate_educational_text(parse_data['user'],parse_data['task'])
#print(result)





# data = {
#     'id': 12,
#     'workLifeRatio': '70:30',
#     'age': 29,
#     'job': '학생',
#     'gender': '남자',
#     'furtherDetails': 'ai 교육과정 수강생',
#     'preferTask': ''
# }

    
# input data 예시 는 위와 같은 형식 task = 'kafka공부하기' timing = '저녁'
def classification_task(data,task,timing):
    load_dotenv()
    
    model_id = 'gpt-4o'
    
    llm = ChatOpenAI(model=model_id, temperature=0, max_tokens=1000)
# Initialize the search tool
    search = DuckDuckGoSearchRun()
    tools = [
        Tool(
            name="DuckDuckGo Search",
            func=search.run,
            description="Useful for searching additional information if given some descriptions."
        )
    ]

    # Initialize the language model
    llm = ChatOpenAI(model=model_id, temperature=0)

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
    )

    # Prepare the prompt
    data_str = "\n".join(f"- {key}: {value}" for key, value in data.items())
    prompt = f"""
    Here is a brief description about a person:
    {data_str}

    Based on the description, provide a persona in few sentences. If it's provided in English, please translate back to Korean. \n
    You can search for more information, such as passion and personality.

    """

    # Run the agent
    persona = agent.run(prompt)

    
    gpt = models.OpenAI(model_id)
    task = 'kafka공부하기'
    timing = '저녁'
    with system():
        lm = gpt + """유용한 개인 비서입니다. 개인적인 성장은 항상 일에 포함됩니다. 작업을 일 또는 삶으로 분류하고 하위 작업으로 세분화하는 데 매우 능숙합니다. 워라벨에 주의를 기울일 수 있습니다."""
    with user():
        llm = lm + f'{persona} 즉 직업, 나이대, 성별 그리고 성격등을 고려하여, 작업을 수행하는 {timing} 시간을 기반으로 {task}을 삶 혹은 일로 분류한 것을 볼드체로 표현해주세요. work인지 life인지만 출력해줘'
    with assistant():
        llm+= gen('분류', save_stop_text = True)

    text = str(llm)
    # Find content between <|im_start|>assistant and <|im_end|>
    # pattern = r'<\|im_start\|>assistant (.*?)<\|im_end\|>'
    match = re.findall(r"\*\*(.*?)\*\*", text)
    if match:
        return match[0]
    return match

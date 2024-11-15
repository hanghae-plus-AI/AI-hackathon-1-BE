from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def generate_subTask(user,task):
    load_dotenv()
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
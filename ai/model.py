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
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from uuid import uuid4
from langchain_core.documents import Document
from datetime import datetime
import os



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

#---------------------


# hack_json = {
#   "id": '8',
#   "title": "AI- 해커톤",
#   "body": "AI 해커톤에 참가하여 프로젝트를 개발하고 발표 준비를 합니다.",
#   "start": 1731651166,
#   "end": 1731658366,
#   "category": "time",
#   'classify': 'work',
#   "subTasks": [
#     {
#       "title": "주제 선정 및 팀 구성",
#       "start": 1731651166,
#       "end": 1731652366,
#       "category": "time"
#     },
#     {
#       "title": "AI 모델 설계 및 데이터 수집",
#       "start": 1731652366,
#       "end": 1731654766,
#       "category": "time"
#     },
#     {
#       "title": "AI 모델 개발 및 테스트",
#       "start": 1731654766,
#       "end": 1731656966,
#       "category": "time"
#     },
#     {
#       "title": "발표 자료 준비",
#       "start": 1731656966,
#       "end": 1731657966,
#       "category": "time"
#     },
#     {
#       "title": "발표 리허설",
#       "start": 1731657966,
#       "end": 1731658366,
#       "category": "time"
#     }
#   ]
# }

class DocumentManager:
    def __init__(self, collection_name="8loMe", persist_directory="./8loMe_chroma_langchain_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=1024,
            api_key=os.environ['OPENAI_API_KEY']
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        
    def convert_to_documents(self, json_data):
        """Convert JSON data to Document objects"""
        documents = []
        sub_tasks = ""
        # Main event document

        
        # Sub-task documents
        for sub_task in json_data["subTasks"]:
            sub_tasks += str({
                "page_content":sub_task["title"],
                "metadata":{
                    "id": f"{json_data['id']}",
                    # "task": json_data["title"],
                    "title": sub_task["title"],
                    # "main_event_title": json_data["title"],
                    "start": datetime.utcfromtimestamp(sub_task["start"]).isoformat(),
                    "end": datetime.utcfromtimestamp(sub_task["end"]).isoformat(),
                    "category": sub_task["category"]
                }
              })
            # documents.append(sub_task_doc)
        main_event_doc = Document(
            page_content=json_data["body"] + sub_tasks,
            metadata={
                "id": json_data["id"],
                "title": json_data["title"],
                "start": datetime.utcfromtimestamp(json_data["start"]).isoformat(),
                "end": datetime.utcfromtimestamp(json_data["end"]).isoformat(),
                "category": json_data["category"],
                'classify': json_data['classify']
            }
        )
        documents.append(main_event_doc)
        return documents
    
    def add_or_update_documents(self, json_data):
        """Add new documents or update existing ones"""
        documents = self.convert_to_documents(json_data)
        event_id = json_data["id"]
        
        # Generate consistent IDs based on event_id
        doc_ids = [f"{event_id}_main"] + [f"{event_id}_sub_{i}" for i in range(len(json_data["subTasks"]))]
        
        # Check if documents with these IDs already exist
        try:
            # Try to get existing documents
            existing_docs = self.vector_store.get(ids=doc_ids)
            if existing_docs and len(existing_docs['ids']) > 0:
                # Update existing documents
                self.vector_store.update_documents(documents=documents, ids=doc_ids)
                print(f"Updated documents for event {event_id}")
            else:
                # Add new documents
                self.vector_store.add_documents(documents=documents, ids=doc_ids)
                print(f"Added new documents for event {event_id}")
        except Exception as e:
            # If there's an error or documents don't exist, add them as new
            self.vector_store.add_documents(documents=documents, ids=doc_ids)
            print(f"Added new documents for event {event_id}")

# 사용 예시
# if __name__ == "__main__":
#     # Initialize document manager
# doc_manager = DocumentManager()

# # Add or update first event
# doc_manager.add_or_update_documents(hack_json)

# # Add or update second event
# doc_manager.add_or_update_documents(hack_json)
#     print(doc_manager.vector_store.as_retriever(search_kwargs={"k": 1}).invoke("AI- 해커톤"))
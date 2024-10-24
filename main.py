from fastapi import FastAPI
from model import new_bid, event, Task
from config import mycollection as mc
import requests

app = FastAPI()

def sendEvent(event : event):
    url = f"http://127.0.0.1:8080/sendEvent/{event.task_id}"
    print(event.dict())
    response = requests.post(url)

    if response.status_code == 200:
        print(response.json()) 

    else:
        print("Error:", response.status_code)
    
@app.post("/newTask/{task_id}")
async def newTask(task_id : int):
    new_task = Task(task_id = task_id)
    mc.insert_one(new_task.dict())
    return {"message" : "inserted new task succesfully"}

    


@app.post("/bid")
async def bid(new_bidding : new_bid):
    data = mc.find_one({"task_id": new_bidding.task_id}) # finding old
    filter = {"task_id": new_bidding.task_id}
    data["task_bids"].append([new_bidding.username,new_bidding.timeStamp,new_bidding.bid]) #adding new bid
    result = mc.replace_one(filter, data)
    print(result)
    new_event = event(task_id = new_bidding.task_id)
    sendEvent(new_event)
    return "done"
    

@app.get("/")
async def root():
    return {"message": "Hello World"}
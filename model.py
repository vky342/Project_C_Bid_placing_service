
from pydantic import BaseModel

class new_bid(BaseModel):
    username : str
    task_id : int
    bid : int
    timeStamp : int

class event(BaseModel):
    task_id : int


class Task(BaseModel):
    task_id: int 
    task_bids: list = []
    final_bid: int = None
    bid_winner: str = None



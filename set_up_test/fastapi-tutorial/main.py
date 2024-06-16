from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional, Annotated, Union
from enum import Enum

app = FastAPI()

@app.get('/')
async def roo():
    return{'message': 'Hello World'}

@app.post('/')
async def post():
    return {'message': 'hello from the post route'}

@app.put('/users')
async def list_users():
    return {'message': 'list all users'}

class FoodEnum(str, Enum):
    pizza = 'pizza'
    pasta = 'pasta'
    salad = 'salad'

@app.get('/foods/{food_name}')
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.pizza:
        return {'food_name': food_name, 'message': 'I love pizza'}
    
class Item(BaseModel):
    name: str
    description: Optional[str] = None #python3.3 to 3.9
    price: int
    #tax: float | None = None #python3.10 or above
    tax: Optional[float] = None

@app.post('/items')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result

# Query is pretty handy when you want to validate query parameters.
# You can also provide default values for query parameters.
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


#how about numerical validation?
#we are gonna use Path
#when the default values is none, the parameter is optional. So, use Query(..., max_length = 10)  
@app.get('/items_validation/{item_id}')
async def read_items_validation(item_id: int  = Path(..., title = 'The ID of the item'),
                                q: Optional[str] = Query(None, max_length = 10, alias='item_query', description='i do not know what this is for, but i just want to use description', title='Query is awesome!!')):
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results

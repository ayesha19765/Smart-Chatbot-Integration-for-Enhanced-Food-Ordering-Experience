app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_root():
    return "<h1>FastAPI Application</h1>"

@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()

        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']

        if intent == "track.order - context: ongoing-tracking":
            return track_order(parameters)
        else:
            return JSONResponse(content={"fulfillmentText": "Unhandled intent"})
    except KeyError as ke:
        error_message = f"Missing required parameter: {ke}"
        return JSONResponse(content={"error": error_message}, status_code=400)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return JSONResponse(content={"error": error_message}, status_code=500)

def track_order(parameters: dict):
    order_id = int(parameters.get('order_id'))  # Use .get() to avoid KeyError if 'order_id' is missing
    order_status = db_helper.get_order_status(order_id)
    if order_status: 
        fulfillment = f"The order status for order id: {order_id} is: {order_status}"
    else: 
        fulfillment = f"No order found with order id: {order_id},{parameters}"
    # print(fulfillment)
    
    return JSONResponse(content={"fulfillmentText": fulfillment})

# track_order({"order_id":53})




import mysql.connector
global cnx
cnx = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="arty!@#$1234",
    database="pandeyji_eatery"
)
def get_order_status(order_id: int):

    cursor = cnx.cursor()
  
    query = ("SELECT status FROM order_tracking WHERE order_id =%s")
  
    cursor.execute(query, (order_id,))

    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    if result is not None:
        return result[0]
    else:
        return None
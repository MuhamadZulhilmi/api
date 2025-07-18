<<<<<<< HEAD
from app.routers import tickets, ticket_categories, ticket_orders, users, auth, accounts, database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
=======
from app.routers import tickets, ticket_categories, ticket_orders, users, auth, accounts, database, online_status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

>>>>>>> b600bb7 (fifth commit)

description = """
Welcome to the Ticketing API! 🚀

This API provides a comprehensive set of functionalities for managing your ticketing platform.

Key features include:

- **Crud**
	- Create, Read, Update, and Delete endpoints.
- **Search**
	- Find specific information with parameters and pagination.
- **Auth**
	- Verify user/system identity.
	- Secure with Access and Refresh tokens.
- **Permission**
	- Assign roles with specific permissions.
	- Different access levels for User/Admin.
- **Validation**
	- Ensure accurate and secure input data.

"""

app = FastAPI(
    description=description,
    title="Ticketing API",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.0.20:3000",
        "http://172.16.13.129:3000",
        "http://172.16.13.129:3001"
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "https://tactic.chatngo.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Ticketing API!"}

<<<<<<< HEAD
app.include_router(tickets.router)
app.include_router(ticket_categories.router)
app.include_router(ticket_orders.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)
app.include_router(database.router)
=======
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.0.20:3000",
        "http://172.16.13.129:3000",
        "http://172.16.13.129:3001"
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3000"
        "https://tactic.chatngo.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Ticketing API!"}


app.include_router(tickets.router, prefix="/api")
app.include_router(ticket_categories.router, prefix="/api")
app.include_router(ticket_orders.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(database.router, prefix="/api")
app.include_router(online_status.router, prefix="/api")
>>>>>>> b600bb7 (fifth commit)

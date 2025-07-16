from app.routers import tickets, ticket_categories, ticket_orders, users, auth, accounts
from fastapi import FastAPI


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


app.include_router(tickets.router)
app.include_router(ticket_categories.router)
app.include_router(ticket_orders.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)

<!-- This assignment was different than any application I've worked on so far! Thank you for the opportunity to learn from this :) -->

### Major issues I identified---
- SQL Injection was a threat
- No input validation or error handling
- Password storage was not secure. Storing plain passwords directly in the db is always a bad idea
- Shared db connection due to the file structure
- No status codes or response consistency!

### Changes I made and why---
- Split app.py into modular files
- Added bcrypt-based password hashing & verification
- Used parameterized SQL queries to prevent injection of malicious code into the db during login
- Added proper error messages & HTTP status codes (so far the easiest change)
- Converted raw SQL tuples into dictionaries for cleaner JSON responses so as to make this into more of an api endpoint
- Added database connection lifecycle via get_db() and killed it with close_db() to cleanup

## Any assumptions or trade-offs---
- Password reset and account lockout are not implemented due to scope
- JWT session management or OAuth not included
- SQLite kept for simplicity, assuming a dev environment

## What you would do with more time---
- Add unit tests
- Add JWT token for login sessions for simplicity in further RESTful implementations (the token can be added to every request so that the backend does not need to store state at all)
- Migrate to SQLAlchemy for easier scaling.
- Add request data validation using Pydantic
- Add rate-limiting and logging

## Which tools you used
-I did use ChatGPT to learn of an approach to handle password encryption, that's how I found out about bcrypt. In the dev work I've done, I have ususally used inbuilt auth such as Firebase, or Clerk for authentication, hence I wasn't aware of a better approach to securing password storage!

<!-- Thank you! Please do check out my other projects too :) Here's one that I have deployed recently: https://get-set-go-five.vercel.app/ -->
# RenewUB
Prototype website built with Flask and PostgreSQL for RenewUB


## Setup 🔨
1. After pulling the repository, create a new ```.env``` file if you do not already have it and add the following: 
```

SECRET_KEY=SOME RANDOM GENERATED HASH

```
**Alternatively if that does not work run the following in console:**
```

export SECRET_KEY=SOME RANDOM GENERATED HASH

```
2. Run the command ``` pip/pip3 install -r requirements.txt ```
2. Create a folder named ```.tmp``` and another file inside called ``` database.db ``` (for SQLite in development)
3. Run the function ``` init_db() ``` **ONCE** in the function ``` index() ``` to build the schemas
4. Go into any SQLite manager (or inside python if you know how) and create a user with a bcrypt-hashed password
5. Done!

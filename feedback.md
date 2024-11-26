# Feedback | Group 1

## Table of Contents

- [Milestone 1 Tasks](#milestone-1-tasks)
- [Milestone 1 Feedback](#milestone-1-feedback)
- [Milestone 2 Tasks](#milestone-2--tasks)
- [Milestone 2 Feedback](#milestone-2--feedback)
<!-- - [Milestone 2 Feedback](#milestone-2--feedback)
- [Milestone 3 Tasks](#milestone-3--tasks)
- [Milestone 3 Feedback](#milestone-3--feedback)
- [Milestone 4 Tasks](#milestone-4--tasks)
- [Milestone 4 Feedback](#milestone-4-feedback)
- [Demo](#demo--20-points)
- [Final Grade](#final-grade) -->

## Milestone 1 Tasks

1. Problem Definition (you can learn more about it [here](https://docs.google.com/document/d/1uUp4Kpduj768tGjAxXGiGrUesQiYIenQoSLlVpRHqpA/edit?usp=drive_link))
2. Finalizing roles [here](https://docs.google.com/spreadsheets/d/1TyMjzzwjN9CZi7VKYZqxUSrDiOfUeaLpuWlcDpUZ8jk/edit#gid=0)
3. Schedule a call/meeting with me and Garo
4. Create a product roadmap and prioritized functionality (items)
5. Create a GitHub repository including `readme.md` and `.gitignore` (for Python) files
6. Create a virtual environment in the above repo and generate `requirements.txt` (ensure `venv` is ignored in git)
   - Create venv: `python -m venv venv`
   - Activate: `source venv/bin/activate`
   - Install: `fastapi`
   - Create `requirements.txt`: `pip freeze > requirements.txt`
   - Deactivate: `deactivate`
7. Push *Problem Definition, GitHub repo setup (readme.md and .gitignore), requirements.txt*
8. Prototype the UI using *Figma* or another similar tool
9. Create a private Slack channel in our Workspace and name it **Group {number}**
10. Install VS Code (also install the Project Manager extension)

## Milestone 1 Feedback

### Problem Definition | 10 points

The problem is defined correctly, and the structure is kept.

- Broad Area of Interest
- Preliminary Research
  - Current trends
  - Opportunities
- Solution with Methodology
  - Data Collection
  - Analytical Techniques
  - Implementation Plan
- Expected Outcomes
- Evaluation Metrics

<span style="color: green;">Grade: 10/10</span>

### Roadmap | 10 points

Can't find the roadmap.

<span style="color: green;">Grade: 0/10</span>


### Administrative Tasks | 5 points

- Roles are assigned
- Preliminary discussion with me was done
- Slack channel is created
- Github Repo is created

<span style="color: green;">Grade: 5/5</span>

### Technical Tasks | 5 points

- Proper `.gitignore` file is available for `Python`
- The `Requirments.txt` file is available with pre-installed packages, indicating that `venv` was created

<span style="color: green;">Grade: 5/5</span>

### Grade

<span style="color: green;">Final Grade: 20/30</span>

---

# Milestone 2 | Tasks 

## Product and Project Manager | 20 points

1. Install `mkdocs` package to start with the documentation (PSS will be available)
2. **Database schema:** Provide your product database structure (ERD)
3. Transform your project file structure according to the below tree.
4. check all the bellow activities from your team and merge everything
   
```bash
PythonPackageProject/ #githhub repo
├── yourapplications/
│   ├── docker-compose.yaml
│   └── .env
│   └── service1/ #postgress
│       ├── .py files # if needed
│       └── Dockerfile # if needed
│   └── service2/ # pgadmin
│       ├── .py files # if needed
│       └── Dockerfile # if needed
|    └── service3/ # etl related
│       ├── .py files
│       └── requirments.txt  
│       └── Dockerfile # if needed
|── example.ipynb # showing how it works
|── docs/ #this folder we need for documentation
|── .gitignore
├── README.md
├── LICENSE
```

## Data Scientist and Data Analyst | 20 points

1. Create a new `git branch` and name it `ds`
2. Simulate the data if you need
3. Try to use the CRUD functionality done by DB Developer
4. Work on modeling part using simple models, conduct extra research
6. Push your works to respective branch
7. Create pull request for the Product Manager
  


## Database Developer | 30 points

1. Create a new `git branch` and name it `db`
2. Create a DB and respective tables suggested by the Product Manager
3. Connect to SQL with Python
4. Push data from flat files to DB
5. Add extra `methods` that you might need throughout the project
6. Push your works to respective branch
7. Create pull request for the Product Manager


## API Developer | 30 points

1. Create a new `git branch` and name it `back`
2. Create a new service and name it `back`
3. Communicate with the DB Developer and PM in order to design the API
4. You can create dummy endpoints in the beginning (PSS will be available)
5. The following endpoints must be available:
   1. GET
   2. POST
   3. PUT
   4. DELETE
6. Push your works to respective branch
7. Create pull request for the Product Manager


# Milestone 2 | Feedback

## Product and Project Manager | 20 Points

1. `MkDocs` isn't installed.
2. The file structure some things are missing the docker files, docker-compose.yaml, yourapplication folder that will have all the services and other files. What you have are the services which are out of the yourapplication folder but there are no docker files in any of them.
3. The ERD seems **correct**.

<span style="color:red">Grade: 5/20</span>

---

## Database Developer | 30 Points

From a database development perspective,there is the database section but I can’t find models.py or schema.py you only created the tables. But for DB creation I don’t want to see SQL queries I want all be created in pythonic way using SQLalchemy library. There is no pgadmin or postgresql.

<span style="color:green">Grade: 10/30</span>

---

## Data Scientist and Data Analyst | 20 Points

The section is there. There should only be the data simulation which I can’t find it there and modeling part which is there. The add, delete, and update should have been in the api part not the database.

The connection to the DB is there but it is done the wrong way .

<span style="color:red">Grade: 5/20</span>

---

## API Developer | 30 Points

There is no API section.

<span style="color:green">Grade: 0/30</span>

---



<span style="color:red; font-weight:bold;">Final Grade: 20/100</span>



# Milestone 3 | Tasks

## Product and Project Manager | 40 Points

1. From the previous milestone, you must have:
   - Refactored the project file structure with services isolated.
   - Updated the ERD diagram to include the missing results table.
   - Applied a new database name across the project.
2. Design all the endpoints required and share them with the Backend and Frontend teams:
   - Ensure the endpoints cover the functionality needed for the web application to work.
3. Support the Frontend Engineer in finalizing the UI (no need to connect with FastAPI within this milestone; this will be done in Milestone 4):
   - Research Streamlit components/elements.
   - Suggest appropriate elements.

**Note**: No need to reinvent the wheel—stick with built-in Streamlit functionality.

---

## Database Developer | 10 Points

1. Update the `database` tables based on the new `ERD` from the previous milestone.
2. Finalize the documentation using proper docstrings.
3. Push the final output to the respective **branch**.

---

## Data Scientist | 20 Points

1. Build the final model.
2. Prepare the final output.
3. Push the final output to the respective **branch**.

---

## API Developer | 30 Points

1. Create **all** the required endpoints (coordinate with the Product Manager).
2. Create schemas using [Pydantic](https://fastapi.tiangolo.com/tutorial/response-model/):
   - **Response Models**: Define the structure of the return values.
   - **Documentation**: Add docstrings to all your endpoints.
3. Push the final output to the respective **branch**.

---
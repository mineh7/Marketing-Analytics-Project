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

# Milestone 2 | Feedback

## Product and Project Manager | 20 Points

1. `MkDocs`  installed and the page is ready.
2. The file structure seems **correct**.
3. The ERD seems **correct**.

<span style="color:red">Grade: 15/20</span>

---

## Database Developer | 30 Points

The database is setup correctly.

<span style="color:green">Grade: 20/30</span>

---

## Data Scientist and Data Analyst | 20 Points

The Data science part is done right and the connection to the DB is there but can't find the prediction table in the DB .

<span style="color:red">Grade: 12/20</span>

---


<span style="color:red; font-weight:bold;">Final Grade: 47/70</span>


# Milestone 3 | Tasks

## Product and Project Manager | 40 Points

1. From the previous milestone, you must have:
   - Refactored the project file structure with services isolated.
   - Updated the ERD diagram to include the missing results table.
   - Applied a new database name across the project.
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

# Milestone 3 | Feedback

## Product and Project Manager | 40 Points
- You have the db and modling in the same service it should be seperate.
- Updated the ERD diagram to include the missing results table seems **correct** but the results table is emtpy.
- I needed to fix your docker-compose file because your code wasn't working.
- Mkdocs is not working.

<span style="color:red; font-weight:bold;">Grade: 15/40</span>

## Database Developer | 10 Points

1. The tables were created but the results table was empty.
2. mkdocs wasn't working.

<span style="color:red; font-weight:bold;">Grade: 5/10</span>

## Data Scientist | 20 Points

1. The final model was the same as previous milestone.
2. Final out put is not shown in the database.

<span style="color:red; font-weight:bold;">Grade: 5/20</span>

<span style="color:red; font-weight:bold;">Fianl Grade: 25/70</span>

# Milestone 4 | Tasks
## Final touches (30)
- **DB Developer:** Implement any database adjustments as required by new visual analytics features.
- **Data Scientist:** Finalize the model and prepare visual outputs for frontend integration.
## Documentation (30 points)
- Create comprehensive documentation using **MkDocs**.
- Each service (e.g., api, app, database, model) should have its own dedicated page with the documentation.
- The first page should provide a high-level overview detailing the **Problem**, **Solution**, and **Expected Outcomes**.
- Host the completed documentation on **GitHub Pages**.
---
## README.md (25 points)
- The `README.md` must be as informative as possible. Include:
  - Weblinks:
    - **MkDocs**
    - **pgadmin**
  - Steps for running the product (check my demo repo).
---
## Repository Management (15 points)
- Clean up the repository to ensure it contains no extraneous files.

# Milestone 4 | Feedback

## Final touches (30)
- **DB Developer:** There is an error in your db creation when running docker-compose.
- **Data Scientist:**you didn't create another service as i wrote you in MileStone 3 feedback.

<span style="color:red; font-weight:bold;">Grade: 10/30</span>

## Documentation (30 points)
- Well Done

<span style="color:red; font-weight:bold;">Grade: 30/30</span>

## README.md (25 points)
- Well Done

<span style="color:red; font-weight:bold;">Grade: 25/25</span>

<span style="color:red; font-weight:bold;">Fianl Grade: 55/85</span>


<span style="color:red; font-weight:bold;">Fianl Grade For all MileStons: 147/255</span>
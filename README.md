

---
# First Code
---

`run both files as you run a simple python code`

### In this folder i have tried to do the following things:
- main.py
    - In this i am trying to make a fastapi logger, in which i stores all the logs that should be printed in console and now storing in a log file.
    - I have use inbuilt python logger and uvicorn logger libraries.
    - I think main problem with the above code is that when using the script logs are stored in a log file and not concurrency showing in the console.
    - All the script is written in layman order, wants to do it in a class format
- custom_logger.py
    - I have made this code so that i can integrate the code to some python script in future
---
# Second Code
---

`run script as "python main.py" `

### In this folder i have tried to do the following things:
- main.py
    - I am running the main script through this file and the reason in that if i want to increase the number of 
        routes in the fastapi, it should be easy to use and bla bla bla
- myapp.py
    - I am doing applying the same logic that i have applied in First_code > main.py
    - But in this script i have tried it to convert it into a class system and it is working
    - But when i was using the script, i faced the problem that, as inbuilt uvicorn logger gives info log level to a every status code and i want to change that
    - So, i added the middleware, which will print the log with correct log level but it is not well defined
    - Due to the above fixed around, i am facing a new problem, in the log, it is printing twice i.e, when i am using my fixed arround and one from the logger. so don't know how to correct it.

---

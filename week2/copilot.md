## How useful did you find the suggestions for code completion?
They were pretty okay, i think they would only work better if there are some doctrings or comments explaining what is intended to be done rather than nothing because otherwise copilot ends up guessing the intended functionality and can suggest rubbish code. 

## Did Copilot have to explanation of the Pylint warning is correct?
Yes the explanation was correct. 

## Did the agent make a working decision, and did the tests?
The agent modified the files and wrote unittests as requires, and also checked that everything ran fine. I manually checked and accepted every command it wanted to run, and also checked on terminal after accepting changed if it actually worked.  

## Is there anything different in the tests from how the tests were done the previous week?
copilot uses some invalid https domain which does not actaully make any https request. The usage of a stub / premade json list is hard to see in the tests but it is done. 

## Did Pylint find errors in the agent's code?
No, not from the agents code. There was an error from the test code copied from the homework paterial in test.py where there was a pylint error that "url" was not capitalized. Copilot did not check or find that. 

## What else did you learn?
I learnt how to use copilot within vscode while coding. I would normally use just web based chat bot and then copy paste. It is very useful for the agent to have access to the entire code context directly
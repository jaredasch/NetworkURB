The code here is just an initial version.

Before next meeting, just try to simulate the following process. Define objects in your project：Fluctuation, Mission, Workflow, Resource. 
For example:

Class Fluctuation has properties:

      category,name.

Class Mission has properties:

      priority,required_workflows[].

Class Workflow has properties: 

      priority(#depends on mission's priority),required_resource[].

Class Resource has properties : 

      category,capacity or availability.
      
F1,F2,F3; #three fluctuations will be ordered randomly, and occur after first mission runs

RS = {R1,R2,R3,R4,R5,R6,R7,R8,R9,R10}

WF = {W1,W2,W3,W4,W5,W6,W7,W8}

#randomly create those match

W1.required_resource = [R1,R2,R3,R4]

W2.required_resource = [R7,R2,R3,R5]

....

W8.required_resource = [R6,R7,R8,R9]

M1.priority = 0

M1.required_workflows = [W1,W3,W5];#randomly create those match, and will be changed by Flucuation F1

M2.priority = 1

M2.required_workflows = [W4,W7,W1];#randomly create those match, and will be changed by Flucuation F2

M3.priority = 3

M3.required_workflows = [W8,W2,W4];#randomly create those match, and will be changed by Flucuation F3

You don't have to totally follow this. It is just a basic image.

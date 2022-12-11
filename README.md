# Robo Auto Script

[![Watch the video](https://img.youtube.com/vi/UwRmSTzJoDI/hqdefault.jpg)](https://youtu.be/UwRmSTzJoDI)
*< click image to watch video or go here [Link](https://youtu.be/UwRmSTzJoDI)!*

## What Does It Do?
  Our app synthesizes code for robots to execute from the English language, using artificial intelligence without human assistance. The GUI provides a user-friendly interface to input commands for the robot to perform. There are two input methods, text, and voice, which take in commands from the user in English. The app handles all translations between high-level English straight to the action executed by the robot. This means that the robot can react to high-level natural language inputs and generate code to complete the command without any hard-coded action. With this new ability made possible by artificial intelligence, robots programmed by this app will be more adaptive, creative, and flexible.
  
## What Inspired Us?
  A great inspiration for our group was the revolutionary DALL-E, an AI system created by OpenAI to generate images through text input. As many of these AI-generated images took the internet by storm, we discovered great opportunities in the implementation of models like this in fields other than art. Researching the technologies and systems that made DALL-E’s achievements possible, we found that Large Language Models (LLMs) were DALL-E’s key to success. Modern LLMs like GPT-3 demonstrate incredible abilities that were unimaginable before their inception and could solve problems seemingly unrelated to language. While continuing our quest to discover more hidden applications of LLMs, we stumbled upon Google’s Research Blogs. One of these blogs revealed an exciting breakthrough: Google’s SayCan. Prior to SayCan, scientists struggled to implement an intuitive, versatile, and intelligent algorithm-planning system into robots. SayCan ingeniously solved this problem, using the PALM language model to generate planned actions for the robot. This LLM had a pseudo-understanding of the world because of the logic that existed within the words of its dataset, the human language. The ability to use LLMs in robotics sparked our imagination, as some of us have experienced problems related to creating efficient programs for robots in our STEM-related courses. We considered using LLMs to develop a strategy to combat these problems. This eventually led to the creation of our app and project.


## Technical Difficulties We Faced
  We faced many technical difficulties as we programmed our app and project. Aside from all of the bugs that came from merge conflicts and refactoring to keep the code base clean, we ran into many issues with compatibility between the robot and our codebase. The first technical issue we encountered was setting up Codex and manipulating the prompt for the model to generate an accurate output. Codex is a LLM trained on a variety of codebases to give it incredible capabilities that allow it to synthesize code. After spending many hours reading the documentation and trying to understand how Codex works, we found the best API calls to utilize and how to format our prompt to get the best results. Another technical issue we encountered was the compatibility of the RobotC compiler, which translates the coding language, RobotC, into code that the machine can understand. The RobotC compiler only ran through the RobotC.exe application, which had to be operated manually with mouse clicks. This limitation prevented us from efficiently automating Codex, voice commands, and the physical robot. We found a solution for this by using a python library to navigate the window GUI interface with preprogrammed commands. Finally, a minor difficulty we encountered was during the implementation of the voice-to-text algorithm. When testing our application in the classroom, we discovered that our algorithm picked up on excess noise from the loud background and the app struggled with getting accurate results. We fixed this problem by getting a better mic and secluding ourselves from the classroom when using our application. 
  
 ## Future Improvements
  Several upgrades can be made to the app to improve its operating speed, versatility, reliability, and accuracy. The most crucial improvement we need to make is to improve the current manipulation of the Codex model through prompt engineering, parameter tuning, and the processing of API calls. By manipulating the model more effectively, we can unlock the true potential of these LLMs. In addition to model manipulation, we can also dramatically improve our hardware and software capabilities. After many years of abuse, some motors are weaker than other motors due to their poor and weathered condition. We can fix this by implementing calibration software for our robot or by getting new hardware. Furthermore, we wish to further improve and streamline the translation process from natural language commands to robot code. By improving our voice recognition software to filter out background noise, we can make the input process much more efficient, practical, and compatible with a wider audience.
  
 


# How to get started
```
pip install -r requirements.txt
```

```
streamlit run 01_🤖_Main.py
```

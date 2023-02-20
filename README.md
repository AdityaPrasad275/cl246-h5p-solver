# cl246-modular-solver

there are two things to any h5p video, navigation and question solving. 
for navigation there are two codes - percentage_extractor.js and navigation.js
for question solving, of which only procedure (code) for multiple choice multiple correct has been developed. for this there is same method implemented
with iframe without iframe. Mostly, without iframe one is used, but if someday console decides it wants to play with iframes, the former can be used.

All these codes are to be inputed into console when the video has been loaded. But console is very notorius in not being able to find any element in a webpage.
For this you have to physically show the console where the element is. Here's a step by step procedure.

#Steps 

##preparing the navigation.js
1) you load the video, do ctrl + shift + i then ctrl + shift + c and hover over to the video (which highlights the video with blue box) and click it. 
2) now run the first line of code in navigation.js (which is commented) and copy paste the result into the 2nd line , let time = 
3) now do ctrl + shift + c and hover over to the dots on the bottom bar of h5p which represent the h5p quiz spots in the video, and then click it.
4) now run percentage_extractor.js and copy paste the result into the 3rd line of navigation.js (let percentage = )

now that navigation.js is prepared, you can use to it jump to right before each h5p question.

##navigating 
1) ctrl + shift + c, hover back to the video and click it (this is to help the console "see" the video)
2) now run the navigator.
3) voila ! you're on the first question (it'll take a second, chill)
4) again, ctrl + shift + c, hover over to the options and click it (this makes console know there are options, so it can click it)
5) check if the question is multiple choice and run the mc_solver.js. if not, solve yourself you dumbass.

voila, you've solved your first question ! now follow an iterative process where you repeat the above steps (only the latter, navigating steps) 
and in each iteration, you increment i in navigation.js till you reach the end of the video !

Enjoy marginally optimizing your h5p solving ! 

maybe in future i'll add some drag and drop solver but until then buh-bye !

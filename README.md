Summary
-
This project was initially inspired after I noticed that my history teacher really liked to say the word massive
Using matplotlib to help display the results, this program hopes to be a tool for analyzing the frequency of words 
in speech.

Help Section
-
This Seciton should outline some of the main commands as well as dependencies to run the program

<b>How to Run</b> <br>
      - Running the software should be as simple as running "py main.py" (or "python main.py") from the command prompt while having the
      necessarry installed software (python and matlibplot)

- <b><i>Commands : </i></b>
  The system currently has a very limited number of commands but can facilitate a still interesting feature set

  <b>open (path)</b> : Opens the text file at the specfied directory and loads it into memory for processing <br> <br>
  <b>find (isCaseSensitive) (word)</b> : Finds the number of appearences of a word in the scanned document. Uppercase C is used to specify the search should be case sensitive
  otherwise the search is assumed to ignore case. <br> <br>
  <b>plot (depth)</b> : Plots the frequency of words up to the depthmost appearing word (E.g. a depth of 10 would return the 10 most used words in the plot)
  and opens them up in a new bar graph. Currently words in this format are sorted case sensitive, this will be an optional flag in the future.

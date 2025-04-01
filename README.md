Summary
-
This project was initially inspired after I noticed that my history teacher really liked to say the word massive.
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

  <b>open (path)</b> : Opens the text file at the specfied directory and loads it into memory for processing <br>
  
  <b>find (isCaseSensitive) (word)</b> : Finds the number of appearences of a word in the scanned document. The search is assumned to be case sensitive unless the flag "c" is passed for case sensitivity
  telling the system to ignore case when finding word instances. <br>

  <b>setBounds (min) (max)</b> Sets the bounds on what words will be displayed based on their frequencies. Minimum Bound determines the first frequency to be displayed in order from greatest to least and max the last frequency. <br>

  <b>plot (isCaseSensitive)</b> : Plots the frequency of words using the flag is case sensitive as "c" to ignore any differences in case between words and "C" (or any other letter) to
  remain case sensitive when plotting data <br>
  
  <b>-exit</b> Exits the program

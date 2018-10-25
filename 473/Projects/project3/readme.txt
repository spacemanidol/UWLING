Ling 473 Project 3 Thai Word Breaking
Daniel Campos 08/21/2018

## Results Just a few lines
<html>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
<body>
คู่ แข่ง ขัน ต่าง ก็ คุม เชิง กัน<br />
เขา เงียบ ไป ครู่ หนึ่ง แล้ว พูด ขึ้น<br />
เธอ หัน มา คุ้ย ทราย ขึ้น มา ใหม่<br />

## Approach
My approach was simple: create a FSM class, add the states based on the rules provided in the assignment and loop over each line. 
My FSM class at each step follows the accept conditions and if the next node will be an end state inserts a ' ' either before or after the character(depending on the specific state). 
At each step the correct result is added to an output string and the last character is removed from the input string. When the input string is len == 0 then our output is ready and we write to a file. 
This process is doen for each line in the file. It would have been easier to turn this all into a large for loop and an if statement but by implementing a FSM class our program can be easily modifiable to deal with any changes in our formal grammar.
The progam opens a write file with the proper encoding, writes the opening html tags and then opens the input file with the proper encoding. It then uses the FSM class for each line in the file outputing proper spacing and final closing html tags
## Special Features
No Special Features
## Missing Features
Not robust to errors in input.

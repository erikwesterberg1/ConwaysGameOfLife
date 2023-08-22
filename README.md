## ConwaysGameOfLife

# Environment & Tools
* Windows 11
* PyCharm by jetBrains
* Python 3.10.0
* Git 2.32 / Git bash for running version control

# Purpose
This project aims to construct a version of Conway's game of life. The game of life is a cellular automation that is played out on, in this case, a 2D grid.
The grid contains a specified number of cells depending on the width and height of the grid. Each cell has either a state of dead, alive or
rim, the latter state is immutable and used by the grid's outermost cells which act as a boarder around the grid. The project is divided in multiple constructions of
algorithms which makes up for the end result, but the main logic corresponds to calculating the state of each cell per generation tick. The program runs by populating the grid based on a predefiened pattern, either loaded from a file or fetch from an inherent method, or randomly generated. Each generation of cells is then calculated based on a set of rules and the result makes up for the next generation of cells. As a complement to the methods which in combine handles the just mentioned logic together with the inherent code which handles output and seed generation, the program also needs to handle exceptions to prevent any abnormal termination of the program.
The goals can therefore be specified as the following:
* Make sure the inputted world size conforms to the specifications, i.e a string containing two positive numbers separated by an x.
* Create a grid which will hold each mutable cell and the border of immutable cells based on the inputted world size.
* Populate the grid with mutable cells based on the inputted seed name using the return value of inherent method get_pattern. Alternatively populate the grid randomly by generating a number between 0 -20, if the number is larger than 16 the cell state will be Alive else dead.
* Populate grid with mutable cells based on the result of reading a specified json file.
* Calculate the next generation of each mutable cell by counting how many alive neighbors it has in the current generation.
* Update the grid with the new generation of cells returned by the calculations of previous goal.


# System design and construction
To verify that the inputted world size conforms to the stated requirements a regular expression is used. Since the objective with this method is to prevent abnormal termination of the program by ensuring that the inputted world size is valid, the string (_args) passed to the method is searched using the following regular expression:
`regex = re.search("^[0-9]+x[0-9]+$", _arg)`.  The regular expression states that if the string doesn’t start and ends with a series of numbers ranging from 0-9 separated by an x, it will return false. This Boolean is then used to raise an assertion error. If the exception is raised, the default world size 80x40 will be used. 
Following the method also checks the loophole which comes with the regular expression in use, namely the world size 0x0. This format will raise a value error by implicitly checking if the values contains 0 or negative values and the default world size will be used in this case also. All of the above logic is done inside a try statement to handle the abnormal termination.

By specifications the world size contains of a with (x) and height (y). The grind is made by calling the product method and passing the range of the world size x and y. This will generate a grid, based on an input of 5x5, that looks like the following:
<br /> **(0, 0) (0, 1) (0, 2) (0, 3) (0, 4)**
<br /> **(1, 0)** (1, 1) (1, 2) (1, 3) **(1, 4)**
<br />**(2, 0)** (2, 1) (2, 2) (2, 3) **(2, 4)**
<br />**(3, 0)** (3, 1) (3, 2) (3, 3) **(3, 4)**
<br />**(4, 0) (4, 1) (4, 2) (4, 3) (4, 4)**<br />
Now we can clearly see the grid and its cells as tuples containing the cells coordinate value. The next objective is to determine the immutable rim cells. By looping the cells produced by the product method and checking if the cell includes a zero or the last value in the range of world size x and y one can conclude that they are the grid’s boundary cells. These cells won’t have any state so let’s assign these value of None. The rest of the loop will handle the actions for setting the state of the mutable cells, thus depending on a specified seed or completely random, as mentioned earlier.

To handle the state of the mutable cells, i.e. the else of the if else statement, the algorithm is using nested if else statement. At this point the program needs to check whether a predefined seed has been passed to the method. If it’s true the cells stored in the variable alive_cells_from_seed is used to match the current cell in the for loop, if it’s a match the state is set to alive, else dead. As the requirements state, we need to fetch these strings from inherent variables which are imported to our working file.
If alive_cells_from_seed is none, the state for each cell in the loop is randomized using randomize_initial_state method which returns either dead or alive based on a randomized number ranging from 0 to 20 where above 16 would result in the latter.
When each mutable cell has been given a state we add it to the dictionary key (the name of the cell as a tuple, more on that below) as a value - "state". 

The name we get from the current cell in the loop, a tuple of coordinates, the state we concluded earlier. The neighbours however have not been explained yet. If we look at the goals, we clearly need to calculate the upcoming generation state of each cell based on the current generations alive neighbours. This is why we set the value neighbours to the return value from the method count_alive_neighbours.
The method simply takes one cell coordinate as argument and returns a list of all cells surrounding the cell in question. This is done by adding and or subtracting one for each coordinate value. Think of the cell (1, 1) in the grid above, the top left neighbour is located at (0, 0) or in this case (x -1, y -1). If we remove the subtraction from x, we end up with the cell below, namely (1, 0) and so forth.
When each cell (key value pair) has been created with a state and a list of neighbours as a dictionary we add it to the population dictionary declared outside the for loop in the populate_world method, like so: <br>`population[cell] = {"state": predefined_state, "neighbours": calc_neighbour_positions(cell)}`</br> and return it after the loop has finished. The result we're looking for should look somewhat like below depending on the world size, in this case a world size of 10x5 with a randomized initial population:<br />
<br />{(0, 0): None, (0, 1): None, (0, 2): None, (0, 3): None, (0, 4): None, (0, 5): None, (0, 6): None, (0, 7): None, (0, 8): None, (0, 9): None, (1, 0): None, <br />
(1, 1): {'state': '-', 'neighbours': [(1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]},<br />
(1, 2): {'state': '-', 'neighbours': [(1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]},<br />
(1, 3): {'state': '-', 'neighbours': [(1, 2), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2)]},<br />
(1, 4): {'state': '-', 'neighbours': [(1, 3), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3)]},<br />
(1, 5): {'state': 'X', 'neighbours': [(1, 4), (2, 4), (2, 5), (2, 6), (1, 6), (0, 6), (0, 5), (0, 4)]},<br />
(1, 6): {'state': '-', 'neighbours': [(1, 5), (2, 5), (2, 6), (2, 7), (1, 7), (0, 7), (0, 6), (0, 5)]},<br />
(1, 7): {'state': '-', 'neighbours': [(1, 6), (2, 6), (2, 7), (2, 8), (1, 8), (0, 8), (0, 7), (0, 6)]},<br />
(1, 8): {'state': '-', 'neighbours': [(1, 7), (2, 7), (2, 8), (2, 9), (1, 9), (0, 9), (0, 8), (0, 7)]},<br />
(1, 9): None, (2, 0): None,<br />
(2, 1): {'state': '-', 'neighbours': [(2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 1), (1, 0)]},<br />
(2, 2): {'state': '-', 'neighbours': [(2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2), (1, 1)]},<br />
(2, 3): {'state': 'X', 'neighbours': [(2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (1, 3), (1, 2)]},<br />
(2, 4): {'state': '-', 'neighbours': [(2, 3), (3, 3), (3, 4), (3, 5), (2, 5), (1, 5), (1, 4), (1, 3)]},<br />
(2, 5): {'state': 'X', 'neighbours': [(2, 4), (3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (1, 5), (1, 4)]},<br />
(2, 6): {'state': '-', 'neighbours': [(2, 5), (3, 5), (3, 6), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5)]},<br />
(2, 7): {'state': '-', 'neighbours': [(2, 6), (3, 6), (3, 7), (3, 8), (2, 8), (1, 8), (1, 7), (1, 6)]},<br />
(2, 8): {'state': '-', 'neighbours': [(2, 7), (3, 7), (3, 8), (3, 9), (2, 9), (1, 9), (1, 8), (1, 7)]},<br />
(2, 9): None, (3, 0): None,<br />
(3, 1): {'state': '-', 'neighbours': [(3, 0), (4, 0), (4, 1), (4, 2), (3, 2), (2, 2), (2, 1), (2, 0)]},<br />
(3, 2): {'state': '-', 'neighbours': [(3, 1), (4, 1), (4, 2), (4, 3), (3, 3), (2, 3), (2, 2), (2, 1)]},<br />
(3, 3): {'state': '-', 'neighbours': [(3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3), (2, 2)]},<br />
(3, 4): {'state': '-', 'neighbours': [(3, 3), (4, 3), (4, 4), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3)]},<br />
(3, 5): {'state': '-', 'neighbours': [(3, 4), (4, 4), (4, 5), (4, 6), (3, 6), (2, 6), (2, 5), (2, 4)]},<br />
(3, 6): {'state': '-', 'neighbours': [(3, 5), (4, 5), (4, 6), (4, 7), (3, 7), (2, 7), (2, 6), (2, 5)]},<br />
(3, 7): {'state': 'X', 'neighbours': [(3, 6), (4, 6), (4, 7), (4, 8), (3, 8), (2, 8), (2, 7), (2, 6)]},<br />
(3, 8): {'state': '-', 'neighbours': [(3, 7), (4, 7), (4, 8), (4, 9), (3, 9), (2, 9), (2, 8), (2, 7)]},<br />
(3, 9): None, (4, 0): None, (4, 1): None, (4, 2): None, (4, 3): None, (4, 4): None, (4, 5): None, (4, 6): None, (4, 7): None, (4, 8): None, (4, 9): None}
<br />The dictionary returned can now be used to print out our first generation to the console, great! By requirements, we need to follow a set of rules for handling the console output. The given pseudocode looks like this:<br />
<br />***FOR EACH generation:<br />
CLEAR console<br />
UPDATE world grid AND STORE new population states<br />
DELAY further execution for 200 milliseconds***<br />
Clear console and delay for 200 milliseconds is rather straight forward and no explanation is needed. The middle part is probably the most important part of the program, and it contains of three methods working togheter, these are:

The dictionary returned can now be used to print out our first generation to the console, great! By requirements, we need to follow a set of rules for handling the console output. The given pseudo code looks like this:<br />
**FOR EACH generation:**<br />
**CLEAR console**<br />
**UPDATE world grid AND STORE new population states**<br />
**DELAY further execution for 200 milliseconds**<br />
Clear console and delay for 200 milliseconds is rather straight forward and no explanation is needed. The middle part is probably the most important part of the program and it contains of three methods working togheter, these are:

* run_simulation - handles the above pseudo code
* update_world - handles printing existing generation to the console and returning the next generation
* count_alive_neighbours - Consist of the rules behind cellular automation, it decides the outcome if the cell in question should be dead or alive in the next generation.

**run_simulation**<br />
At first, the initial thought when studying the pseudocode is to implement this iteratively. However, an option is to execute this using a recusive approach, which of course is more of a challenge.
To implement the run_simulation method recursively, the first thing we need to do is figuring out the base case. Let's assume there's five generations, we pass nth_generation (5 in this case) and our population as parameter to the recursive method. Now the first thing we will have to do is match nth_generation against our base case which would be the last return of next_generation, that is when we hit zero we should start popping stack frames of the call stack visualized below.
<br />update_world - call_nr_1 ((next_generation)after this, base_case is hit, and we return population)
<br />update_world - call_nr_2 (next_generation)
<br />update_world - call_nr_3 (next_generation)
<br />update_world - call_nr_4 (next_generation)
<br />update_world - call_nr_5 (population)<br />
As we can see we continuously call update_world, the first time we run it we print out the initial population, thereafter we make use of count_alive_neighbours and returns the next generation which will be printed out in the next call.<br />

**update_world**<br />
As mentioned above, update world will handle the printing to the console and return the next generation. To print each cell to the console requirements state that we need to use inherent methods progress() and get_print_value(). So we simply need to loop through all cells state and pass it to the get_print_value which act as an argument to progress. The tricky part here is that we need to keep in mind to print out a new break, otherwise the method would print out all values in a long row. This we can keep track of by checking the looped cells y value. If the value is equal to our world size y value we know that we need to insert a line break. The logic is handled by if statements, if it's a cell without state i.e. a rim cell, we print out the get_print_value of rim. Else, we get the state and print out that value and most importantly we know that these cells are mutable, and we need to account for their future state. This we do by calling count_alive_neighbours and which returns the amount of alive cells the current cell has, then we call another method which returns the new state as a string. Mow that we have the new state we can simply make a copy of each cell in the loop and add it to a new dictionary which we will use as return value, our new generation.

**count_alive_neighbours**<br />
count_alive_neighbours is used to determine the future of each cell. As we know each mutable cell has a property containing a dictionary of state and neighbours. All we need to do is loop through the list of neighbours and count how many of them are alive using a counter. To execute this we also need the current generation so that we can access each neighbours state, this we need to do since the property neighbours is only a list of cell coordinates. So we loop through the list of neighbours and get the property state if the current neighbour has one, i.e. is mutable. If it is mutable and has a state of alive in the current generation we increment our counter by one which we in the end return. Now we know how many alive neighbours we have but one thing is still missing, we need to decide what to do with this information. This is where the method change_state, which we mentioned earlier comes in. The method looks like this:<br />
`def change_state(alive_neighbours: int, cell_props: dict) -> str:`<br />
    `cell_state_was = cell_props['state']`<br />
    `if cell_state_was == cb.STATE_ALIVE:`<br />
        `if alive_neighbours < 2 or alive_neighbours > 3:`<br />
            `return cb.STATE_DEAD`<br />
        `else:`<br />
            `return cb.STATE_ALIVE`<br />
    `if cell_state_was == cb.STATE_DEAD:`<br />
        `if alive_neighbours == 3:`<br />
            `return cb.STATE_ALIVE`<br />
        `else:`<br />
            `return cb.STATE_DEAD`<br />
This is the algorithm that makes the whole program run, the rules are simple. If the state is alive and has two to three alive neighbours it will stay alive. If it has less than two alive neighbours it will die due to underpopulation, if it has more than three, it will die due to overpopulation. Lastly a dead cell will only come to life if it has exactly three alive neighbours. And this is what we are implementing with the source code above, we check what state the cell had and decide the new state based on the number of alive neighbours.

Now there is only one goal that hasn't been explained, that is how we can load a seed from a JSON file, let's look at the pseudocode.
<br />**FORMAT file name**<br />
**OPEN file AND RETRIEVE population data**<br />
**MAKE SURE retrieved data conforms to required data types**<br />
**RETURN population AND world size as tuple**<br />

To format the file name we need to account for different operating systems as well as IOerrors. The challenge is easily solved with the help of pythons path lib library. We make a cross-functional file path with the use of the Path method. When this is done we can proceed to opening and reading the file. This is done with the use of the with: open method inside a try statement to prevent abnormal termination of the program. Using the with: open method we do not need to actively close the reader as well which is handy. Now we can't just read anything, first of all we need to pass the path created and the r for read to the open method. With this done all we need to do is stored the read data using the "json.load" method. The json files are given as part of the project and consist of to properties, world_size and population. All we need to do is store these of these properties values, and we can then process them. The world size we don't need to process any other than casting it to a tuple, the population however we need to process. The values in population can be seen as a dictionary, however due to the JSON format we can simply return them. To solve this one can use a method ast.literal_eval which will return the correct datatype if the string passed contains of a python literal structure. In this case it will evaluate the string passed as a tuple which is exactly what's needed but this is only done for the "key" in the dictionary. We also need the correct format for the state and neighbours from the population. This is solved by mapping each neighbour in the list provided to a tuple.Now that all values are in the correct format we can simply return the result as a tuple which is stated by the requirements and the last piece of logic is done.

# Validation
_Make sure the inputted world size conforms to the specifications, i.e a string containing two positive numbers separated by an x._<br />
This part of the program has been validated by triggering the exception handlers. If we intentionally input a world size not conforming to the regular expression we are left with an assertion error and the assert message can be read in the terminal.
When the command ran without a proper x value, like so: `$Python -m Project.gol -ws Ax100 -g 100` the assert message provided was: _World size should contain width and height, separated by ‘x’. Ex: ‘80x40’” 
using default size: 80,40_. This was further tested by multiple intentionally wrong world size inputs which all resulted in the same error. As additional validation of world size a value error was implemented, this was mainly implemented to cover the loophole of the regular expression i.e. the zero by zero sizing. This error was reproduced using the command `$Python -m Project.gol -ws 0x0 -g 100` which threw the error message: _Both width and height needs to have positive values above zero_.<br /><br />
_Create a grid which will hold each mutable cell and the border of immutable cells based on the inputted world size._
_Populate the grid with mutable cells based on the inputted seed name using the return value of inherent method get_pattern. Alternatively populate the grid randomly by generating a number between 0 -20, if the number is larger than 16 the cell state will be Alive else dead._<br />
By requirements the grid should contain of x amount of cells given the size of the world, two examples (80x40 = 3200 cells, 120x80 = 9600 cells) are given which was used to validate the size of the grid. When debugging the populate_world method passed with the example sizes, the size or length of the dictionary containing the cells was inspected. The result conforms with the expected results, namely `population = {dict: 3200}` respectively `population = {dict: 9600}`. The immutable cells where also validated using the formula (width*2)+(height*2)-4, the expected result based on a world size of 10x5 where 26. By counting each immutable cell in the return dictionary from the populate_world method the result where matching the expectation.
Besides validating the world size, the population by seed, file and randomization also where matched against the visual aid provided by project documentation. As the program results in something visual it was fairly easy to determine the correctness, at least when it came to the predefined pattern loaded from seed and seed_file. All that needed to be done was to match the first population with the images from the project documentation as well as study that the next generation was conformed with the expected new pattern. This was done by creating a grid on paper and drawing out the initial population of each pattern where green dots represented alive cells and red dead cells. After that the second and third generation was manually calculated and drawn on paper to act as a key to validate a program run with a generation of three. The behavior of the randomized pattern was mainly validated by stepping through each method inside the populate_world method and making sure all values where not abnormal, i.e. way to many alive cells to begin with and as well as an abnormal reproduction from each generation. To help stating a normal cell reproduction videos was also studied with the help of the vido platform YouTube, mainly a video by Numberphile from 2014 (https://www.youtube.com/watch?v=R9Plq-D1gEk&t=350s).<br />
<br />_Populate grid with mutable cells based on the result of reading a specified json file._
<br />The result of this method (load_seed_from_file) was validated with the help of it's IOexception handler which threw an error message like this when an unrecognised file input was given: _File does not exist, make sure flag input ({file_name}) corresponds to the seed file in question_. If the file specified in the command was found we automatically knew the path was correct, on Windows at least. For the other operating systems, the path unfortunately couldn't be tested due to lack of hardware, in this case I had to rely on the pathlib documentation.
<br />
<br />_Calculate the next generation of each mutable cell by counting how many alive neighbors it has in the current generation._
<br />The count_alive_neighbours method was validated by debugging the program using breakpoints. First of all the list of neighbours needed validation, as we know all mutable cells have eight neighbours so by counting the list length of the cell property neighbours one could confirm that we weren't counting to many neighbour to begin with. With this in mind it was only a matter of stepping through each row of cells and make sure that the method returned a correct amount of alive neighbours.
The return value was then used to create a copy of the cell with the help of the change_state method visualized above. the result of these methods was also validated by inspecting the returned dictionary from the update_world method as well as inspecting the terminal output which was mentioned in the "populate world" validation. If the pattern visible in the terminal matched the pattern drawn on paper, I could conclude that the methods worked properly.
<br />
<br />_Update the grid with the new generation of cells returned by the calculations of previous goal._
<br />This part is mainly handling the terminal output and if something was abnormal it would have been quite obvious while running the program. By running the program with the command `$Python -m Project.gol -s pulsar -g 100` the output validates the expected result. One part which I struggled with was that I was not only adding the copy of the cell with the new state to the new generation dictionary, but the dictionary passed as argument as well. This resulted in an abnormal cell reproduction and was quickly solved by thoroughly inspecting each step of the forloop inside the update_world method.


# Discussion
**This part will mainly discuss the future improvements as well as struggles along the way.**<br />
First of all I would like to say that my implementations should not be considered as final. I am sure there is a lot of improvements that can be done, especially when in comes to reducing the lines of code. I know there are places, for instance in my populate_world methods that is very repetitive. This part is only one the improvements I would like to suggest. Another part is where the cells neighbours are set, here we can see that the solution can be implemented in a much more elegant way, preferably by using a loop.
I would also like to comment the code more detailed to assist readability and make it easier to come back to the project for further development. This was of lower prioritization and much time for refactoring and comments where taken by providing this detailed readme, which of course act as a way of describing the project in an even more detailed way. However, it would be nice to complement with hints and aid in the source code. When it comes to struggles, the main problem I encountered was the handling of the data loaded from seed-file. I did a lot of manually casting and splitting, replacing etc. to get it to work properly. In the end I managed to reduce the code by approximately 10 lines using the ast.leteral_eval function which was very pleasing. I also managed to refactor the populate_world method to use the python product function instead of using a nested for loop, which came in very handy. Both these task took a lot of unnecessary tinkering, but both events resulted in great learning. Initially I also used an object-oriented way to create the first population, this ofcourse did not conform with the project specification and was completely missed by my part. In the end I think the object-oriented approach i.e. creating a custom class and instantiate every cell as an object was rather unnecessary. The fix also required approximately 10 minutes of work which plus the time of the actual development of the class in the first place. All in all, even though the fix was rather fast it was time I could have spared by reading the project documentation more thoroughly. In the end I am quite happy with the result.

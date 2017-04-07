# control script
Refer to [our sketch](./Step2-README.md) for a high level overview of what we are trying
    to implement with the control script.
    
##### Instruction 1
Copy the start of script from `skeletons/control-skeleton.py` to the current directory
    as `control-script.py`.
Read over the skeleton to make you understand what it already implements.
Make sure that you can run it and that you see the output that you expect to see.

## First step - get the name of the downloaded file from downloader to the parser

### Variables and "name binding"
In python we "bind" values to variable names. You have probably guessed that the 
    `=` sign is used to bind a value (on the right side of the `=`) to a name
    on the left side.
Programmers say that `=` is the "assignment" or "name binding" operator, the name is
    the left operand and the value is the right operand.

Sometimes we use a variable just to make the code more concise and readable.
For example, in Python the standard way to refer to the mathematical constant Pi
 is to `import math` and then use `math.pi` in your code. 
Pi is approximated as 3.141592653589793 in that representation (at least on my computer).
We use `math.pi` instead of that literal numeric notation for clarity and conciseness.

Occassionally we have variables that are not known when we write the code, but they
    will be fixed to constant value at runtime.
`SCRIPT_NAME` and `VERBOSE_MODE` are 2 examples of this type of variable.
It may seem strange to call them variables, but they are stored in python in the same way
    as a name that has a changing variable.

The most common variables that we encounter are names that can refer to different values
    over the course of the program.
We can use `=` operator to bind these variables.

We also bind a value to a name when we call a function and pass in an object as an argument.
For instance if we call the `warn` function in the skeleton script:

    warn("this is a warning")

the quoted string is called a literal string - because we are telling Python literally
    what value we want.
If we look at the definition of `warn`,
we do not see any code that says `msg="this is a warning"`.
However, when we execute that code, part of the process of "calling" a function in 
    Python is to bind the values passed in to the names used in the function definition.

We can assign variable with literals:
    x = 5

Or by referring to another variable or part of another variable:

    x = y
    SCRIPT_PATH = sys.argv[0]

Python executes the instructions in a function definition whenever the function is "called".
If the function has a `return` statement, then execution of the function stops there and
   the resulting value of the function is whatever was returned.
We often capture this returned value, by binding it to a variable.
An example of this in the skeleton script is:

    decorated_message = "{} WARNING: {}\n".format(SCRIPT_NAME, msg)

A method is just like a function that is associated with a certain type of data.
That example uses a method of the `str` type.
We could have also written this as:

    decorated_message = str.format("{} WARNING: {}\n", SCRIPT_NAME, msg)

Other "operators" are similar to function calls, but they are harder to spot because
    they don't have a name then parentheses.
For instance, in the example script the terse operator syntax is used: 

    VERBOSE_MODE = '--verbose' in sys.argv

This is really just a shorthand for:

    VERBOSE_MODE = list.__contains__(sys.argv, '--verbose')

using "function" syntax or:

    VERBOSE_MODE = sys.argv.__contains__('--verbose')

using "method" syntax.

As we'll see in the next step, we can also bind a name to a value in `for` loop.

##### Instruction 2
At the bottom of the skeleton, we can call the functions defined earlier in the script.
Start the pipeline by calling (first_sp, second_sp, third_sp):`download_query_data` and `parse_queries_from_csv` in the 
correct order.

Note (from the "docstring" comments for the functions) that the second one needs to know
    the filepath to the csv file, and the first function returns that information.

Also know, that `parse_queries_from_csv` is returning the list of queries, so we'll need
    to capture that value for the next steps in the pipeline.

## Second step: loop over all of the queries
### Iteration with a `for` loop
Repeating a task is a crucial part of programming.
The syntax:

    for x in some_collection:
        print(x)
    print("done")

is an example of a simple Python loop. 

All that is required for this code to work is for the variable name `some_collection` to
    be bound to some "iterable" object.
Python has some builtin data structures that are obviously collections:
  * a Python `list` are ordered collections of items - iteration over a `list` returns each element in order.
  * a Python `set` is an unordered collection of items where an item cannot be repeated - 
    iteration over a `set` will return each element, but the programmer should not assume
    anything about the order in which the items will be encountered.
  * a Python `dict` is an unordered collection of key-value pairs. The keys must be unique.
  Iteration is similar to iteration of the `set` of keys. If `d` is a `dict` you can also use
  `d.keys()` to iterate over the keys, `d.values()` to iterate over the values or `d.items()`
  to iterate over key-value pairs.

But even strings in python are iterable.
If you had `some_collection = "hello"` before the loop
above, then the output would be:

    h
    e
    l
    l
    o
    done

(this would also be the output if you had `some_collection = ["h", "e", "l", "l", "o"]`)

Our `for` loop is really a terse syntax for 4 instructions:
  1. Start walking through each element in the collection `some_collection`
  2. If there are more elements in the iteration over the collection, 
     perform a name-binding operation that is
     equivalent to `x = ` with the next element in the collection as the right operand.
     If there are no more elements we exit the loop.
  3. Now execute the body of the loop (the indented block).
  4. Go back to step 2

"Exit the loop" in step 2 means to continue execution of the code after the indented block.

##### Instruction 3
Write a `for` loop to iterate over our queries. You can start by just printing out each query.
You can also use a syntax like `print(type(x))` to print out the name of the data type 
    for the value that is bound to the variable x.

Run the code to make sure you get as many lines as you expected and that the printed values
were what you expected.

##### Instruction 4
Add the calls to `get_phylogeny_according_to_open_tree` and 
     `get_phylogeny_according_to_wikipedia` to your `for` loop.

While we are still working on the code it is probably best to have the code write out
    the results of these operations using the `debug` function to show messages like:

    control-script.py: Open Tree returned 1
    control-script.py: Wikipedia returned 2

Can you figure out how to use the python string formatting to do this?

Remember that you need to run the script with the `--verbose` command line flag to 
    activate the `debug` messages!

## Step 3: Accumulate the results
We are actually close to done implementing the sketch, but our sketch is vague with respect
to how we summarize the data.
For any query for set of 3 species and a web service we could have 1 of 3 outcomes:
  1. The service identifies the species that is furthest from the others (write 1, 2, or 3 to
  its stdout),
  2. the service doesn't know (writes 0), or the service failed
  3. exit code non-zero

So, after running all of the queries, we should probably report, 
the number of queries for which:
  1. both services failed,
  2. Open Tree failed, and Wikipedia gave the "I don't know" response,
  3. Open Tree failed, but Wikipedia identified the most distant species,
  4. Wikipedia failed, and Open Tree gave the "I don't know" response,
  5. Wikipedia failed, but Open Tree identified the most distant species,
  6. Open Tree said "I don't know", and Wikipedia identified the most distant species,
  7. Wikipedia said "I don't know", and Open Tree identified the most distant species,
  8. Both said "I don't know",
  9. Both identified a most distant species, and they disagreed.
  10. Both identified a most distant species, and they agreed.

Sounds tedious. It will be tedious if you want the full results.

I'm OK with you just storing the number of times at least one query failed to return
    a definitive response (the sum of 1-8 above) and the number of agreements and disagreements.
That would be only 3 resulting counts not 10.


#### results as separate variables
You can do this by setting up 10 counter variables starting at 0, such as:

    both_failed = 0
    ot_fail_w_idk = 0
    ...
    both_agreed = 0


#### results as a dict
Or you could use a dictionary so that the results object is a single object to be passed
    around:
    
    results = {"both failed": 0,
               "ot fail w idk": 0,
               ...
               "both agreed": 0
              }

#### results as a defaultdict
Or you can get fancy and use a Python `defaultdict` which allows you to say that whenever
    you access a key that is not in the dict give it a certain default value. 
We could use 0 as our default:

    from collections import defaultdict
    r = defaultdict(lambda: 0)

then later you can do things like:
    r["both failed"] += 1

to add 1 to the value associated with the key "both failed".
If you did that on a normal dict that lacked the "both failed" key, then you'd see 
    an error as a python exception.
But with a defaultdict, it would just pretend that the key had been stored with the default
    value of 0.

#### results as a list of lists and a couple of extra variables
There is even some elegance to:

    # Treat OT as the first index, and Wikipedia as the second.
    
    FAILED = 0
    DONT_KNOW = 1
    CHOSE_MOST_DISTANT = 3
    results = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
              ]
    num_agreed, num_disagreed = 0, 0

because you'd be set up to do things like this later:

    ... (SOME CODE HERE) ...
        OT_OUTCOME = FAILED
    ... (SOME CODE HERE) ...
        WIKI_OUTCOME = CHOSE_MOST_DISTANT
    ... (SOME CODE HERE) ...
    
    # Notice how elegant our storing of the result is here.
    results[OT_OUTCOME][WIKI_OUTCOME] += 1
    
    # unfortunately we want to have more details than just whether they
    #   both succeeded in chosing a most distant species...
    if OT_OUTCOME == CHOSE_MOST_DISTANT and WIKI_OUTCOME == CHOSE_MOST_DISTANT:
       if OT_TREE == WIKI_TREE:
           num_agreed += 1
       else:
           num_disagreed += 1
    
##### Instruction 5
I don't really care how you do it.
Just make sure to initialize a results structure to all 0 counts before the loop.

##### Instruction 6
OK, now we need to interpret the results of the queries to each service and store
them in our results counting data structure.

### Conditionals
I've shown an `if` but have not talked about it. 
The basic structure is:

    if some_test():
        a_code_block()
        to_be_executed_if_some_test_returned(True)
    elif other_fn() == 5:
        another_code_block()
        to_be_executed_if_first_test_returned_False()
        and_other_fn_returned_5()
    else:
        code_to_be_executed_if_both_tests_evaluated_False()

both an `elif` and `else` block are optional.

Note that once again code blocks are preceded by `:` and are indented.

Notice that `==` is a test for equality (while `=` was the name binding operator)

##### Instruction 7
Use conditionals to process the return values of the query functions to correctly update
your counts.


## Step 4: print the results

##### Instruction 8
Pass your results counters in to the `write_summary` function and then use
string formatting an print statements two write them to standard output in an
interpretable manner.

##### Instruction 9
Run it. Do you see the results that make sense give our mock function?



## Step 5: write a real parser
OK now we need to do the real stuff, not just use the mock functions.

First lets parse the example input in our `parse_queries_from_csv` function.

If `fn` is a filepath we can do the following:

    with open(fn, "r") as input_stream:
        for line in input_stream:
            # line will be bound to a string ending with a newline here.
            line_without_extra_whitespace = line.strip()
            print(line_without_extra_whitespace)

to print every line in a file.

If we have a list of queries initialized to an empty list before this loop, then
    we can use the `append` method of a list to add another item to the list.

If we have a string called `y`, and we want to break it into a list of words where a comma is
    the separator, then we can use `broken = y.split(",")`

Note that if you had a list `q` then the "slice" denoted `q[1:]`
    would be a new list that omits the first element (the `q[0]` element).

##### Instruction 10
Can you use that info to fill in the body of `parse_queries_from_csv` function?

Remember that we need to skip the header row, and only store the second, third and fourth
columns of each row (the first is the submitter's initials).

## Step 5: call the other tools
The python `subprocess` module is very helpful for running other tools.
For instance:

    import subprocess
    command_to_run = ["echo", "5"]
    try:
        raw_output = subprocess.check_output(command_to_run)
    except:
        print("called script failed!")

Would store the standard output from the `echo` program run with 1 command line argument `5`.

If the called process exits with a non-zero exit code, then an exception is raised.
That is why we put the `check_output` call in a `try: ... except:` block.

If we know that our query scripts write nothing but an integer to stdout if they succeed, then
we can use:

    num_written = int(raw_output)

to coerce the input from a Python string to a Python integer.

If you are calling another python script, recall that Python is really the executable.

    command_to_run = [sys.executable, path_to_script, arg_one, arg_two, arg_three ]

is the standard way to use the same version of Python to run the script whose path is stored
    in the variable `path_to_script`.

##### Instruction 11
Let's assume that we use the names:
  * download-google-sheet-as-csv.py
  * query-open-tree.py, and 
  * query-wikipedia.py
as the scripts written by the other tasks in this project.

Finish the control script by replacing the placeholder code in `download_query_data`,
`get_phylogeny_according_to_open_tree`, and `get_phylogeny_according_to_wikipedia`.

If the other groups are not down, you can test with `skeletons/mock-query.py`.
Take a look at that code
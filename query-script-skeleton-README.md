## Getting you started...

I'd start with the following skeleton of a program:

    import sys
    command_line = sys.argv
    
    sys.stderr.write("The raw command line was {}\n".format(command_line))
    quoted_command_line_parts = '" "'.join(command_line)
    sys.stderr.write("quoted_command_line_parts = {}\n".format(quoted_command_line_parts))
    quoted_command_line = '"{}"'.format(quoted_command_line_parts)
    sys.stderr.write("quoted_command_line = {}\n".format(quoted_command_line))
    
    sys.stderr.write('The command line was:\n  {}\n'.format(quoted_command_line))
    had_error = False
    
    # Add your code here to set a value for tree_integer_code or set had_error to True
    # if you have an error use:
    #    sys.stderr.write("some descriptive error message")
    # to emit helpful messages to the user (or control script).
    
    if had_error:
        sys.exit(1)
    sys.stdout.write(tree_integer_code)
    sys.stdout.write('\n')
    
If you should see some output about the command line and then an error like:

    Traceback (most recent call last):
      File "query-open-tree.py", line 20, in <module>
        sys.stdout.write(tree_integer_code)
    NameError: name 'tree_integer_code' is not defined

because we have not written the code in the middle.

Pass in different command line arguments to make sure that you understand:
  * [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)
  * the funky Python trick of using `"sep".join(["a", "b"])` to convert lists to strings.
     See the [function docs](https://docs.python.org/3/library/stdtypes.html?highlight=str.join#str.join)
  * the basics of [python string formatting](https://docs.python.org/3/library/stdtypes.html?highlight=str.join#str.format)
  * we push error messages and diagnostic messages as strings to standard error
     with `sys.stderr.write`. We use `sys.stdout.write` for the core output of our script.
  * single or double quoted string literals can be used
  * `\n` in a string literal encodes a newline character.

Note that in Python, when a script reaches the end, Python will exit with exit code of 0
(indicating success).
We could add `sys.exit(0)` at the end, but it  is not necessary.

## Making sure you get three species names.
Adding

    arguments = sys.argv[1:]
    assert len(arguments) == 3, "Expecting 3 species names as arguments"
    first_name, second_name, third_name = arguments

somewhere near the top (but after `import sys`) is a very quick way to:
  1. remove the path the the script as the first argument.
  2. Exit with error non-zero error code and a decent error message if the user
   fails to give the script 3 strings as arguments.
  3. Assign the variables `first_name`, `second_name`, and `third_name` to hold the names.


Now you can return to either:
  * [./query-wikipedia-README.md](./query-wikipedia-README.md#Next)
  * [./query-open-tree-README.md](./query-open-tree-README.md#Next)
#!/usr/bin/env python
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

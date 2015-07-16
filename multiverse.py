"""

INSTRUCTIONS

This written content is stored in a data file in JSON format so it can
be easily reused. If you just want to read it, this Python 2
script reads the content from the JSON data file and converts it into an
HTML file which can be read using any web browser. For further information on
this system:

http://github.com/vijithassar/multiverse-json

First, identify the file containing the content for which you'd like to generate a
readable version. It's most likely located in the same folder as this script,
and ends with the file extension .json

Next, open a terminal window and navigate to the directory containing this
script.

Finally, to build the readable HTML file, type the following command; omit the dollar
sign and the brackets, but include the .json file extension of the data file.

$ python multiverse.py [type the source data file's name here]

The script will create a new HTML file in this directory, named after the base
filename of the source data file (and/or overwrite the previous version, if it
exists). The terminal window should tell you the exact name of the file, and then
you can open it in any web browser.

"""

import sys
import json
from pprint import pprint

# parse input arguments
input_filename = sys.argv[1]
if len(sys.argv) > 2:
    # allow alternate compilation modes; unused for now
    mode = sys.argv[2]
else:
    mode = 'default'
output_filename = input_filename.split('.')
extension = output_filename.pop()
# if we have a json file, name the output file to match
if (extension == 'json'):
    output_filename = ''.join(output_filename) + '_' + mode + '.html'

# read json file
def read_json(file):
    with open(file) as contents:
        json_data = json.load(contents)
    return json_data

# write string to file
def write_results(filename, content):
    with open(filename,'w') as file:
        file.write(content)

def expand_attributes(attrs):
    attributes = {}
    attributes['classes'] = []
    attributes['other'] = []
    attributes_string = ''
    # for each attr
    for attr in attrs:
        # expand shorthand hash to id
        if (attr[0:1] == '#'):
            attributes['id'] = attr[1:]
        # expand shorthand dot to html class
        elif (attr[0:1] == '.'):
            attributes['classes'].append(attr[1:])
        # include anything else as is
        else:
            attributes['other'].append(attr)
    # build all expanded attribute strings into a single
    # attribute string which we can use when building the
    # html
    if 'id' in attributes:
        attributes_string += ' id="' + attributes['id'] + '"'
    if (len(attributes['classes']) > 0):
        attributes_string += ' class="' + ' '.join(attributes['classes']) + '"'
    if (len(attributes['other']) > 0):
        attributes_string += ' ' + ' '.join(attributes['other'])
    # trim whitespace
    attributes_string = attributes_string.strip()
    if (len(attributes_string) > 0):
        return attributes_string
    else:
        return False

def should_return_self(key):
    key_fragments = key.split('.')
    first_key = key_fragments[0]
    # if splitting with dots has no effect, we're just dealing with a string
    # to be skipped
    has_dot = '.' in key
    has_space = ' ' in key
    dot_first = False
    if (has_dot and has_space):
        space_first = key.index(' ') < key.index('.')
    else:
        space_first = True
    # see if the key is in the documentation object
    if first_key in multiverse_content:
        no_match = False
    else:
        no_match = True
    if (no_match and space_first):
        return True
    else:
        return False

# look up a piece of documentation given its location
def get_multiverse_piece(input_string):

    # if it is a reference, parse into attributes
    if (input_string[:6] == 'refer@'):
        input_elements = input_string.split(' ')
        key = input_elements[0][6:]
        attrs = input_elements[1:]
    # otherwise proceed without attributes
    else:
        key = input_string
        attrs = []

    # if there are additional attrs, expand them to full html
    # strings
    if (len(attrs) > 0):
        attributes_string = expand_attributes(attrs)

    # attach the attribute string to span tags
    pre = ''
    post = ''
    if 'attributes_string' in locals():
        # if we have an attribute string, add it with a span
        # tag to avoid injecting unexpected line breaks
        pre = "<span " + attributes_string + '>'
        post = "</span>"

    # split input key string into an iterable list of items
    # using javascript-style dot notation
    lookup = key.split('.')

    # return the input string immediately if there's nothing to look up
    if (should_return_self(key)):
        return input_string

    # open a string into which we'll build our HTML
    multiverse_piece = ''
    # start iterating at the root level of documentation
    target = multiverse_content
    # for each item in the lookup table
    for index, level in enumerate(lookup):
        next_target_exists = index + 1 < len(lookup)
        # if there's a next lookup element
        if (next_target_exists):
            # if it's currently a dictionary
            if ((type(target) is dict)):
                # advance one level deeper
                target = target[level]
        # if we're at the last lookup table element
        else:
            # and this is currently a dictionary
            if (type(target) is dict):
                # perhaps the key leads to a string
                if (type(target[level]) is unicode):
                    # in which case we'll wrap it in an array
                    content_list = [target[level]]
                # or perhaps the key leads to a list
                elif (type(target[level]) is list):
                    # alias it for syntactic clarity
                    content_list = target[level]
                # for each item in the list
                multiverse_piece = ''
                multiverse_piece += pre
                for content_item in content_list:
                    # is it a reference?
                    if (content_item[:6] == 'refer@'):
                        # recursively run this function, wrapped in new attribute spans
                        # if necessary
                        multiverse_piece += get_multiverse_piece(content_item)
                    else:
                        # if it's not a reference, then we just add the string
                        multiverse_piece += content_item
                multiverse_piece += post
    # return the sum of all string additions
    return multiverse_piece

# get the documentation
multiverse_data = read_json(input_filename)
# get the compilation order; this can be more flexible in the future
compilation_sequence = multiverse_data['metadata']['versions'][mode]
# alias the documentation content for syntactic clarity
multiverse_content = multiverse_data['root']

# a string into which we'll glue all extracted text
results = []
# run documentation lookup for every element in the compilation order
for compilation_key in compilation_sequence:
    multiverse_string = get_multiverse_piece(compilation_key)
    results.append(multiverse_string)

multiverse_instructions = '<div class="multiverse-instructions">' + multiverse_data['metadata']['instructions'] + '</div>'
results.append(multiverse_instructions)

# print to console for debugging/development purposes
results_string = ''.join(results).encode('utf-8').strip()

# save results to file
write_results(output_filename, results_string)

print('Content successfully built! Everything from the ' + input_filename + ' source data file has been written into the more readable ' + output_filename + ' file, which you can now open in any web browser.')

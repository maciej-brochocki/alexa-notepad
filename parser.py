#!/usr/bin/env python


def parser(data, command):
    # defaults
    new_data = None
    response = "command not supported"

    # decompose data
    if data is not None:
        lines = data.split('\n')
        del lines[-1]
    else:
        lines = []

    # decompose command
    tokens = command.split(' ')
    action = tokens[0]
    del tokens[0]

    if action == "add":
        if len(tokens) == 0:
            response = "no note to add"
            return new_data, response
        lines.append(" ".join(tokens))
        new_data = "\n".join(lines) + "\n"
        response = "note added"

    elif action == "search":
        if len(lines) == 0:
            response = "no data to search"
        else:
            if len(tokens) == 0:
                response = "no keywords to search"
                return new_data, response
            response = ""
            for l in lines:
                match = True
                for t in tokens:
                    if l.find(t) == -1:
                        match = False
                        break
                if match is True:
                    if response == "":
                        response = l
                    else:
                        response += ". " + l
            if response == "":
                response = "nothing found"

    elif action == "read":
        if len(lines) == 0:
            response = "no data to read"
        else:
            if len(tokens) == 0:
                return new_data, response #defaults
            if tokens[0] == "all":
                response = ". ".join(lines)
            elif tokens[0] == "oldest":
                response = lines[0]
            elif tokens[0] == "latest" or tokens[0] == "newest":
                response = lines[-1]
            else:
                return new_data, response # defaults

    elif action == "delete":
        if len(lines) == 0:
            response = "no data to delete"
        else:
            if len(tokens) == 0:
                return new_data, response #defaults
            if tokens[0] == "all":
                lines = []
            elif tokens[0] == "oldest":
                del lines[0]
            elif tokens[0] == "latest" or tokens[0] == "newest":
                del lines[-1]
            else:
                return new_data, response # defaults
            response = "data deleted"
            if len(lines) == 0:
                new_data = ""
            else:
                new_data = "\n".join(lines) + "\n"

    return new_data, response

if __name__ == '__main__':
    try:
        with open('data.txt', 'r') as myfile:
            data = myfile.read()
    except IOError:
        data = None
    new_data, response = parser(data, "search how")
    print "new data:\n", new_data
    print "response:\n", response
    if new_data is not None:
        with open('data.txt', 'w') as myfile:
            data = myfile.write(new_data)

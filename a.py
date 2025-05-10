"""
<> = param
() = optional OR dependend on previous params
**  = multiple values
-- = extra, does not count when given AND is given
--nocom = no comformation for command
--ignoreperms = ignore permission errors, WORKS ONLY IN ELEVATED MODES!!
--ignorerrors = ignore errors, for ex. file delete file --ignorerrors: Ignores errors like directory has files or subdirs.

goto <int> (<int>) #first is line, second is char
run <program> <file>

'''
file <info | write | overwrite | visual | append | replace | read | clean | rename | delete | create> <filepath> (name) (line | list[line,
line..]) (<plaintext>)
--copy --nocon --ignorerrors
write <filepath> <line | list[lines]> <plaintext>
overwrite <filepath> <overwrite> <file> <plaintext>
visual <filepath>
append <filepath>
replace <filepath> <line> <plaintext>
read <filepath> (<line>)
clean <filepath>
rename <filepath> <name>
delete <filepath>
create <filepath> <plaintext>
'''

#for read is the line the int OR list of int that it will read, when no line(s) is/are given it reads the whole file that
for clean, delete and overwrite a confirmation is required!   Name is only an option when rename is choosen as mode
func <>
if <condition> <func> <else>
elif *<condition> <func>*
while <condition> <func> <break>
for <var | x> <int | list | str |var> <func>
add *<int>*
div *<int>*
mul *<int>*
sub *<int>*
average <*<int>* | list>
modus *<int>*
len <int | list | str |var>
var <set | get | del | create> <var> (<value>)
varlist
cd <path | subdir>
dirs (<path | subdir>)
files (<path | subdir>)

help <func>
print <str | var>
open <filepath | subdir> (<program | filepath>)  #if program not given, use standard program instead for ex. open file.txt notepad.exe
tree <path | subdir>
clear
shutdown <int | var | bool | > --nocom #when var is true, the system shuts down, int is time in seconds before shutdown
disk <list | format> (<volume | disk>)
elevate <int>
delevate <int>
quit
exit
task <list | kill | search | visual> (<value>)
cmd <command (with params)>
sort <list>
equation <solvefor> <equation>
convertvar <value> <type>
decode <key1> <key2> <offset> <encrypted>
encode <key1> <key2> <offset> <plaintext>
dir <move | make | remove | rename | clone> <path | subdir> (<path | subdir>) (<path | subdir>) (<name>) --nocom --ignorerrors --ignoreperms
calc *<number> <+ | - | * | / | ** | //>*
clone <path> <path>
error <raise | list | search> (<qwuery>) (<raiseExepctionCode>) #query can be errorcode/int or errorname/str
commands (<command>) --help --info #when command is NONE, it gives all the commands in the system for this language, if given, it return the
command ORfunctioncode and info
translate <inputtext> <orignal-lang> <translate-lang> (<deeple | google>) #service can be deeple, google...


"""
import typing as typ
import shlex
from pathlib import Path
def dynamic_class_call(class_name):
    class_map = {cls.__name__.lower(): cls for cls in globals().values() if isinstance(cls, type)}
    return class_map.get(class_name.lower())

def list_dir_contents(path="."):
    path = Path(path)
    return [item.name for item in path.iterdir()]

def parse_command(command: str) -> list:
    if command.strip() == "":
        return "newline"
    parts = shlex.split(command)
    if not parts:
        return []

    cmd = parts[0].lower()

    # Handle known commands with custom parsing
    try:
        if cmd == "goto":
            return [cmd, int(parts[1])]

        elif cmd == "run":
            return [cmd, parts[1], parts[2]]

        elif cmd == "file":
            filepath = parts[2]
            mode = parts[1].lower()
            if mode in ("overwrite", "replace", "visual","write"):
                line = int(parts[3])
                content = " ".join(parts[4:])
                return [cmd, filepath, mode, line, content]
            elif mode in ["read"]:
                line = int(parts[3])

            else:
                content = " ".join(parts[3:])
                return [cmd, filepath, mode, content]

        elif cmd == "func":
            return [cmd]

        elif cmd == "if":
            return [cmd, parts[1], parts[2], parts[3] if len(parts) > 3 else None]

        elif cmd == "elif":
            return [cmd, parts[1], parts[2]]

        elif cmd == "while":
            return [cmd, parts[1], parts[2], parts[3] if len(parts) > 3 else None]

        elif cmd == "for":
            return [cmd, parts[1], parts[2], parts[3]]
        elif cmd == "calc":
            expr = " ".join(parts[1:])
            return [cmd, expr]

        elif cmd in {"add", "sub", "mul", "div", "modus"}:
            return [cmd, int(parts[1])]

        elif cmd == "average":
            return [cmd] + parts[1:]

        elif cmd == "len":
            return [cmd, parts[1]]

        elif cmd == "var":
            action = parts[1]
            varname = parts[2]
            value = parts[3] if len(parts) > 3 else None
            return [cmd, action, varname, value]

        elif cmd == "varlist":
            return [cmd]

        elif cmd == "cd":
            return [cmd, parts[1]]

        elif cmd == "dir":
            return [cmd]

        elif cmd == "files":
            return [cmd] + parts[1:]

        elif cmd == "help":
            return [cmd, parts[1]]

        elif cmd == "print":
            return [cmd, parts[1]]

        elif cmd == "rename":
            return [cmd, parts[1]]

        elif cmd == "open":
            return [cmd, parts[1]]

        elif cmd == "tree":
            return [cmd, parts[1]]

        elif cmd == "remdir":
            return [cmd, parts[1]]

        elif cmd == "mkedir":
            return [cmd, parts[1]]

        elif cmd == "movedir":
            return [cmd, parts[1], parts[2]]

        elif cmd == "clear":
            return [cmd]

        elif cmd == "shutdown":
            return [cmd, parts[1] if len(parts) > 1 else None]

        elif cmd == "cleandisk":
            return [cmd, parts[1]]

        elif cmd == "elevate":
            return [cmd, int(parts[1])]

        elif cmd == "delevate":
            return [cmd, int(parts[1])]

        elif cmd == "delete":
            return [cmd, parts[1]]

        elif cmd in {"quit", "exit"}:
            return [cmd]

        elif cmd == "task":
            return [cmd, parts[1], parts[2]]

        elif cmd == "cmd":
            return [cmd, " ".join(parts[1:])]

        elif cmd == "sort":
            return [cmd, parts[1]]

        elif cmd == "equation":
            return [cmd, parts[1], parts[2]]

        elif cmd == "convertvar":
            return [cmd, parts[1], parts[2]]

        elif cmd in {"decode", "encode"}:
            return [cmd, parts[1], parts[2], parts[3], parts[4]]

        elif cmd == "copydir":
            return [cmd]

        else:
            return [cmd, *parts]
    except:
        return []
class decoder():
    def __init__(self, data, prompt: str):
        self.data: dict = {}
        self.prompt: str = prompt
        self.feedback = None
        contents = parse_command(prompt)
        if contents == "newline":
            self.feedback = ""
            return
        if not contents:
            self.feedback = "In valid command"
        elif contents[0] == "error":
            pass
        elif contents[0] == "file":
            self.feedback = file(contents).return_()
        elif contents[0] == "help":
            self.feedback = help(contents).return_()
        elif contents[0] == "calc":
            self.feedback = calc(contents).return_()
        elif contents[0] == "files":
            self.feedback = files(contents).return_()
        else:
            self.feedback = f"Command '{contents[0]}' not implemented."


    def get(self):
        return (self.feedback)

class EXAMPLECLASS():
    def __init__(self, param: list):
        self.param = param
        self.feedback = None
        pass

    def return_(self):
        return self.feedback

    def procces(self):
        pass
    @staticmethod
    def help(self):
        return ["",""]


class help():
    def __init__(self, param: list):
        self.param = param
        self.feedback = None
        self.function = ''
        self.procces()

    def write(self):
        pass

    def return_(self):
        return self.feedback

    def procces(self):
        if len(self.param) < 2:
            self.feedback = "Error: No function specified for help."
            return
        self.function = self.param[1]
        cls = dynamic_class_call(self.function)
        self.feedback = "\n".join(cls(None).help(cls)) if hasattr(cls, 'help') else f"No help available for '{self.function}'."


class sub():
    def __init__(self, param: list):
        self.param = param
        pass

    def write(self):
        pass

    def return_(self):
        return

    def procces(self):
        pass

class calc():
    def __init__(self, param: list):
        if param:
            self.param = param
            self.feedback = None
            self.procces()
            pass

    def return_(self):
        return self.feedback

    def procces(self):

        self.feedback = eval(self.param[1])




        if False:self.feedback

    @staticmethod
    def help(self):
        return ["A command used for calculating multiple numbers. Supports *: multiplication, /: division, +: addition, -: substraction, "
                "x**y: x to the power of y, x//y: perfect division and (): brackets","Usage:"]

class files():
    def __init__(self, param: list):

        self.param = param
        self.filepath = param[1] if len(param) >= 2 else "."
        self.feedback = None
        self.procces()
        pass

    def return_(self):
        return self.feedback

    def procces(self):
        folder = Path(self.filepath)
        self.feedback = "\n".join([f.name for f in folder.iterdir() if f.is_file()]) + "\n"



        pass
    @staticmethod
    def help(self):
        return ["",""]

class add():
    def __init__(self, param: list):
        self.param = param
        pass

    def write(self):
        pass

    def return_(self):
        return

    def procces(self):
        pass


class goto():
    def __init__(self, param: list):
        self.param = param
        pass

    def write(self):
        pass

    def return_(self):
        return

    def procces(self):
        pass


class file():
    def __init__(self, param: list = None):
     if param:
        self.param = param
        self.mode = param[1]
        self.filepath = Path(param[2])
        self.flags = param[-1] if isinstance(param[-1], list) else []
        self.callback = None
        self.procces()

    def return_(self):
        return self.callback

    def procces(self):
        try:
            if self.mode == "write":
                lines = eval(self.param[3]) if self.param[3].startswith("list[") else [int(self.param[3])]
                content = self.param[4]
                self.write_lines(lines, content)

            elif self.mode == "overwrite":
                target_file = Path(self.param[3])
                content = self.param[4]
                with open(self.filepath, "w") as f:
                    f.write(content)

            elif self.mode == "visual":
                self.callback = self.filepath.read_text()

            elif self.mode == "append":
                with open(self.filepath, "a") as f:
                    f.write("\n")

            elif self.mode == "replace":
                line = int(self.param[3]) - 1
                content = self.param[4]
                lines = self.filepath.read_text().splitlines()
                lines[line] = content
                self.filepath.write_text("\n".join(lines) + "\n")

            elif self.mode == "read":
                self.callback = ''
                self.callback += '""""""\n\n'
                if len(self.param) > 4:
                    line = int(self.param[3]) - 1
                    lines = self.filepath.read_text().splitlines()
                    self.callback += lines[line] if 0 <= line < len(lines) else "Line out of range"
                else:
                    self.callback += self.filepath.read_text()
                self.callback += '\n\n""""""'


            elif self.mode == "clean":
                if "--nocon" not in self.flags:
                    input(f"Are you sure you want to clean {self.filepath}? (y/n): ")
                self.filepath.write_text("")

            elif self.mode == "rename":
                new_name: str = self.param[3]
                if new_name.strip()  == "": return "Filename is empty or only spaces."
                if new_name == self.filepath.name: return "Filename is the same as the current one."
                self.filepath.rename(self.filepath.with_name(new_name))

            elif self.mode == "delete":
                if "--nocon" not in self.flags:
                    con = input(f"Are you sure you want to delete {self.filepath}? (y/n): ")
                    if con in ["yes","y","1"]:
                        pass
                    else:
                        return "No permission from user to delete the file"
                self.filepath.unlink()
            elif self.mode == "create":
                new_name: str = self.param[3]
                if len(self.param) <= 4: pass

            else:
                self.callback = f"Invalid mode: {self.mode}"

        except Exception as e:
            if "--ignorerrors" in self.flags:
                self.callback = f"Ignored error: {e}"
            else:
                self.callback = f"Error: {e}"

    def write_lines(self, lines, content):
        existing = self.filepath.read_text().splitlines() if self.filepath.exists() else []
        for line in lines:
            idx = int(line) - 1
            if idx < 0 or idx > len(existing):
                continue
            existing.insert(idx, content)
        self.filepath.write_text("\n".join(existing) + "\n")
    @staticmethod
    def help(self):
        return [
            "file <write | overwrite | visual | append | replace | read | clean | rename | delete> <filepath> ...",
            "Gebruik flags zoals --nocon of --ignorerrors waar van toepassing"
        ]


class mult():
    def __init__(self, param: list):
        self.param = param
        self.feedback = None
        pass

    def return_(self):
        return self.feedback

    def procces(self):
        pass
    @staticmethod
    def help(self):
        return ["",""]


while True:
    prompt = input("C:/<StateFlow>: ")
    stdout = decoder("",prompt).get()
    print(stdout)
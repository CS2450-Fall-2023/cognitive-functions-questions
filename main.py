'''
This is just a TUI to interact with the `personality` module

To traverse the questions in a more general way, it might be easier to
put traversal code in the `Question` class in ther future. Maybe
create a new `QuestionWrapper` class, which holds a `Question` tree.
`QuestionWrapper` would have `advance` and `previous` methods to
traverse the tree. `main`, or any GUI/TUI/anyone using the package would
only every interact with the `QuestionWrapper` class.

This is just one possibility, though.
'''
from personality import Question
from text_format import TextFormat as Fmt
from typing import List, Optional
import json
import os

QUESTIONS = "questions.json"
RESULTS = "result_info.json"
EXIT_PHRASES = ["exit", "e"]
BACK_PHRASES = ["back", "b"]

def main() -> None:
    question = Question(json.load(open(QUESTIONS)))
    results = json.load(open(RESULTS))

    print(question.title)

    usr_in = ""
    prompt = f"Enter " + Fmt.BOLD + f"`{EXIT_PHRASES[0]}`" + Fmt.END 
    prompt += " to quit, or type "+Fmt.BOLD + f"`{BACK_PHRASES[0]}`" + Fmt.END + " to go to the previous question"
    
    value_stack: List[str] = []
    invalid_input = lambda inp : Fmt.BOLD + Fmt.RED + f"{inp} is not a valid input." + Fmt.END
    err: Optional[str] = None

    # Running the TUI
    while True:
        # clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt)
        # Reached a terminal state
        if len(question.children) == 0:
            personality_type = ''.join(value_stack)
            print(Fmt.BOLD + Fmt.UNDERLINE + f"{personality_type} - {results[personality_type]['title']}:" + Fmt.END + ":")
            print(results[personality_type]["content"])
        else:
            for i, q in enumerate(question.children):
                print(Fmt.RED+f"{i + 1}: "+Fmt.END+Fmt.BOLD+Fmt.UNDERLINE+f"{q.title}"+Fmt.END)
                print(f"{q.content}\n\n")
        
        if err is not None:
            print(err)
            err = None

        usr_in = input("> ")
        if usr_in in EXIT_PHRASES:
            break;
        
        # Going back:
        if usr_in in BACK_PHRASES:
            if question.parent is not None:
                # make sure to pop the values from the value_stack:
                for _ in question.values:
                    value_stack.pop()
                question = question.parent
                continue
            err = Fmt.BOLD + Fmt.RED + "You are at the top question. You cannot go back." + Fmt.END
            continue

        # Going forward
        try:
            answer_value = int(usr_in) - 1 # Answers are given 1-indexed :)
        except ValueError:
            err = invalid_input(usr_in)
            continue
        
        if answer_value < 0 or answer_value >= len(question.children):
            err = invalid_input(usr_in)
            continue

        # Go forward in tree
        question = question.children[answer_value]

        # Push to the stack
        for val in question.values:
            value_stack.append(val)


if __name__ == "__main__":
    main()

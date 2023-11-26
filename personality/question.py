from typing import Optional, List, Any, Tuple

class Question:
    '''
    `Question` is a tree class. It contains a parent (for the user to be able to
    go back) and follow up questions top the current one. It also contains a question
    `title` string, and a `content` string.
    '''
    def __init__(self, questions, parent: Optional["Question"]=None) -> None:
        self.title: str = questions["title"]
        self.content: str = questions["content"]
        self.values: List[str] = questions["values"]

        self.parent = parent
        self.children: List["Question"] = []

        for child_question in questions["questions"]:
            self.children.append(Question(child_question, parent=self))

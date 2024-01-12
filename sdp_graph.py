class Dependency:
    def __init__(self, label, head, tail, words) -> None:
        self.label = label
        self.head = head
        self.tail = tail
        self.words = words

    def __str__(self) -> str:
        # if words is None:
        #     return f"<{self.label}: {self.head} --> {self.tail}>"
        if self.label == "*TOP*":
            return f"<TOP: _root_ --> {self.words[self.tail]}>"
        return f"<{self.label}: {self.words[self.head]} --> {self.words[self.tail]}>"


class SDP:
    def __init__(self, string):
        self.table = [line.split("\t") for line in string.split("\n")]
        self.table.pop()

        self.words = []
        self.lemma = []
        self.pos = []
        self.dependencies = []

        self.load_words()
        self.load_links()
    
    def load_words(self):
        self.preds = []
        for i, row in enumerate(self.table):
            self.words.append(row[1])
            self.lemma.append(row[2])
            self.pos.append(row[3])

            if row[4] == '+':
                self.dependencies.append(Dependency("*TOP*", -1, i, self.words))
            
            if row[5] == '+':
                self.preds.append(i)
        return
    
    def load_links(self):

        for i, row in enumerate(self.table):
            for j in range(6, 6 + len(self.preds)):
                if row[j] != '_':
                    self.dependencies.append(Dependency(row[j], self.preds[j - 6], i, self.words))

        return
    
    def __str__(self) -> str:
        return "\n".join(map((lambda dep: str(dep)), self.dependencies))


class SDP2:
    def __init__(self, string):
        # print(string)
        self.table = [line.split("\t") for line in string.split("\n")]
        # self.table.pop()

        self.words = []
        self.dependencies = []

        self.load_words()
        self.load_links()
    
    def load_words(self):
        for row in self.table:
            if len(row) >= 2:
                self.words.append(row[1])
            else:
                print(self.table)
        return
    
    def load_links(self):
        for i, row in enumerate(self.table):
            if row[2] != '_':
                for j, head in enumerate(row[2].split("|")):
                    label = row[3].split("|")[j][5:]
                    self.dependencies.append(Dependency(label, int(head)-1, i, self.words))
        return
    
    def __str__(self) -> str:
        return "\n".join(map((lambda dep: str(dep)), self.dependencies))
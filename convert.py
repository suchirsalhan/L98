from sdp_graph import *

def read_file(path):
    f = open(path, encoding="utf8")

    sentences = {}
    current = ["", ""]

    for line in f.readlines():
        if line != "\n":
            if line[0] == "#":
                if current[0] != "":
                    sentences[current[0]] = current[1]
                current[0] = int(line[1:])
                current[1] = ""
            else:
                current[1] += line

    sentences[current[0]] = current[1]
    return sentences

def convert_from_output(string):
    data = []
    for sentence in string.split("\n\n"):
        if sentence != "":
            data.append(SDP2(sentence))
    return data

def convert_from_semeval14(data):
    sentences = {}
    for key, val in data.items():
        sentences[key] = SDP(val)
    return sentences

def convert_to_semeval14(sentences, sentences_to_ids, gold):
    data = {}
    for val in sentences:
        idx = sentences_to_ids[" ".join(val.words)]
        gold_ex = gold[idx]

        preds = []
        for dep in val.dependencies:
            if dep.head not in preds and dep.label != "*TOP*":
                preds.append(dep.head)
        
        preds.sort()
        
        table = []
        for i, word in enumerate(val.words):
            row = [str(i+1), word, gold_ex.lemma[i], gold_ex.pos[i], "-"]
            # row.append("+" if top == i else "-")
            row.append("+" if i in preds else "-")

            for _ in range(len(preds)):
                row.append("_")

            table.append(row)
        
        for dep in val.dependencies:
            if dep.label == "*TOP*":
                table[dep.tail][4] = "+"
            else:
                head_col = preds.index(dep.head)
                table[dep.tail][6 + head_col] = dep.label
        
        out = ""
        for row in table:
            out += "\t".join(row) + "\n"

        data[idx] = out
    return data

def convert_to_semeval15(data):
    output = ""

    for key, val in data.items():
        output += "#" + str(key) + "\n"

        for row in val.table:
            row.insert(6, 'frame')
            output += "\t".join(row) + "\n"
    
        output += "\n"

    return output

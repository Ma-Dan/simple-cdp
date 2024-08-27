import ahocorasick

class DFA:
    def __init__(self, words):
        self.words = words
        self.build()

    def build(self):
        self.transitions = {}
        self.fails = {}
        self.outputs = {}
        state = 0
        for word in self.words:
            current_state = 0
            for char in word:
                next_state = self.transitions.get((current_state, char), None)
                if next_state is None:
                    state += 1
                    self.transitions[(current_state, char)] = state
                    current_state = state
                else:
                    current_state = next_state
            self.outputs[current_state] = word
        queue = []
        for (start_state, char), next_state in self.transitions.items():
            if start_state == 0:
                queue.append(next_state)
                self.fails[next_state] = 0
        while queue:
            r_state = queue.pop(0)
            for (state, char), next_state in self.transitions.items():
                if state == r_state:
                    queue.append(next_state)
                    fail_state = self.fails[state]
                    while (fail_state, char) not in self.transitions and fail_state != 0:
                        fail_state = self.fails[fail_state]
                    self.fails[next_state] = self.transitions.get((fail_state, char), 0)
                    if self.fails[next_state] in self.outputs:
                        self.outputs[next_state] += ', ' + self.outputs[self.fails[next_state]]

    def search(self, text):
        state = 0
        result = []
        for i, char in enumerate(text):
            while (state, char) not in self.transitions and state != 0:
                state = self.fails[state]
            state = self.transitions.get((state, char), 0)
            if state in self.outputs:
                result.append((i - len(self.outputs[state]) + 1, i))
        return result

dfa = None

def init_filter_1(filename):
    global dfa
    words = []

    f = open(filename)
    lines = f.readlines()
    for line in lines:
        words.append(line)
    f.close()

    dfa = DFA(words)

def filter_words_1(text):
    global dfa
    result = []
    for start_index, end_index in dfa.search(text):
        result.append((start_index, end_index))
    for start_index, end_index in result[::-1]:
        text_filter = text[:start_index] + '*' * (end_index - start_index + 1) + text[end_index + 1:]
    return text_filter, text == text_filter

A = None
def init_filter(filename):
    global A
    words = []
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        words.append(line)
    f.close()
    A = ahocorasick.Automaton()
    for index, word in enumerate(words):
        word = word.replace('\r', '').replace('\n', '')
        A.add_word(word, (index, word))
    A.make_automaton()

def filter_words(text):
    global A
    result = []
    for end_index, (insert_order, original_value) in A.iter(text):
        start_index = end_index - len(original_value) + 1
        result.append((start_index, end_index))

    text_filter = text
    for start_index, end_index in result[::-1]:
        text_filter = text[:start_index] + '*' * (end_index - start_index + 1) + text[end_index + 1:]
    return text_filter, text != text_filter


if __name__ == '__main__':
    text = '我是一个来自星星的超人，具有超人本领！'
    words = ['超人', '星星']
    res = filter_words(text, words)
    print(res)  # 我是一个来自***的***，具有***本领！
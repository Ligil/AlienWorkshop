class Question:
    def __init__(self, userId, questionId, question, time):
        self.__userId = userId
        self.__questionId = questionId
        self.__question = question
        self.__time = time

        #admin side
        self.__answer = None #Store reply here
        self.__display = False #Whether to display on public page

    def get_userId(self):
        return self.__userId
    def set_userId(self, userId):
        self.__userId = userId
    def get_questionId(self):
        return self.__questionId
    def set_questionId(self, questionId):
        self.__questionId = questionId
    def get_question(self):
        return self.__question
    def set_question(self, question):
        self.__question = question
    def get_answer(self):
        return self.__answer
    def set_answer(self, answer):
        self.__answer = answer
    def get_display(self):
        return self.__display
    def set_display(self, display):
        self.__display = display
    def get_time(self):
        return self.__time
    def set_time(self, time):
        self.__time = time

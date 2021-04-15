class Review:
    def __init__(self, reviewId, reviewText, stars, userId, timePosted, profileFilename):
        self.__reviewId = reviewId
        self.__reviewText = reviewText
        self.__stars = stars
        self.__userId = userId
        self.__timePosted = timePosted
        self.__profileFilename = profileFilename
        self.__filename = None

    def get_reviewId(self):
        return self.__reviewId

    def get_reviewText(self):
        return self.__reviewText
    def set_reviewText(self, reviewText):
        self.__reviewText = reviewText

    def get_stars(self):
        return self.__stars
    def set_stars(self, stars):
        self.__stars = stars

    def get_userId(self):
        return self.__userId
    def set_userId(self, userId):
        self.__userId = userId

    def get_timePosted(self):
        return self.__timePosted
    def set_timePosted(self, timePosted):
        self.__timePosted = timePosted

    def get_filename(self):
        return self.__filename
    def set_filename(self, filename):
        self.__filename = filename

    def get_profileFilename(self):
        return self.__profileFilename
    def set_profileFilename(self, profileFilename):
        self.__profileFilename = profileFilename

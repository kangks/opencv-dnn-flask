
class BoundingBox(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return str(self.__dict__())

    def __repr__(self):
        # return f'Data[{self.id}]'
        return str(self.__dict__())

    def __dict__(self):
        d = {
                "x": self.x,
                "y": self.y,
                "w": self.w,
                "h": self.h
            }
        return d

class PredictionDto(object):

    def __init__(self, x, y, w, h, label, classId, score):
        self.label = label
        self.classId = classId
        self.score = score
        self.bbox = BoundingBox(x,y,w,h)
        # self.bbox.y = y
        # self.bbox.w = w
        # self.bbox.h = h

    def __str__(self):
        return str(self.__dict__())

    def __repr__(self):
        # return f'Data[{self.id}]'
        return str(self.__dict__())

    def __dict__(self):
        d = {
                "label": self.label,
                "classId": self.classId,
                "score": self.score,                
                "bbox": self.bbox.__dict__()
            }

        # if(not self.extractedInformation is None):
        #     d["extractedInformation"] = {}
        #     if(len(self.extractedInformation.nric) > 0):
        #         d["extractedInformation"]["nric"] = o.extractedInformation.nric

        #     if(len(self.extractedInformation.creditcard) > 0):
        #         d["extractedInformation"]["creditcard"] = o.extractedInformation.creditcard

        return d
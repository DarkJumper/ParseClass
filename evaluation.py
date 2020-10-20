import pandas as pd


class _project:
    def __init__(self, project):
        self.project = project.strip().split(";")

    def getDF(self):
        Version_Date = "{0}.{1}.{2} : {3}.{4}.{5}".format(
            self.project[6],
            self.project[7],
            self.project[8],
            self.project[9],
            self.project[10],
            self.project[11],
        )
        Creation_Date = "{0}.{1}.{2} : {3}.{4}.{5}".format(
            self.project[6],
            self.project[7],
            self.project[8],
            self.project[9],
            self.project[10],
            self.project[11],
        )
        df_dict = {
            "Name": self.project[1],
            "Kommentar": self.project[2],
            "Ersteller": self.project[3],
            "Firma": self.project[14],
            "Version": Version_Date,
            "Erstellung": Creation_Date,
        }
        return pd.DataFrame(df_dict, index=[0])


class _area:
    def __init__(self, areas):
        self.areas = areas[1:-1]

    def getDF(self):
        df_dict = {}
        for count, line in enumerate(self.areas, start=-len(self.areas) + 1):
            list_for_dict = [
                line.strip().split(";")[4],
                2 ** abs(count),
            ]
            df_dict.update({line.strip().split(";")[2]: list_for_dict})
        return pd.DataFrame(df_dict)


class Evaluation:
    status = True

    def __init__(self, *args):
        if len(args) > 7:
            print("zuviel Daten Übergeben")
            self.status = False
        else:
            self.project = _project(args[0])
            self.area = _area(args[1])

    def getAreaDf(self):
        return self.area.getDF()

    def getProjectDF(self):
        return self.project.getDF()


# from readFile import *
# from parsingFreelance import *


# filepath = "/Users/peterschwarz/VS Code Projekte/ParseClass/elektrolyse_20200326.csv"
# input = WorkWithFile(read, filepath).execute()
# parsed_data = Freelance(input).get_data()
# Evaluation(*parsed_data).getProjectDF()

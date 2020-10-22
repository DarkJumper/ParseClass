import pandas as pd
import numpy as np


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
        return pd.DataFrame.from_dict(df_dict, orient="index")


class _area:
    def __init__(self, areas):
        self.areas = areas[1:-1]

    def getDF(self):
        df_dict = {}
        for count, line in enumerate(self.areas, start=-len(self.areas) + 1):
            splitted_line = line.strip().split(";")
            list_for_df = [
                splitted_line[4],
                2 ** abs(count),
            ]
            df_dict.update({splitted_line[2]: list_for_df})
        return pd.DataFrame.from_dict(df_dict, orient="index")


class _var:
    def __init__(self, varia):
        self.varia = varia[1:-1]

    def getDF(self):
        df_dict = {}
        for line in self.varia:
            splitted_line = line.strip().split(";")
            list_for_df = [splitted_line[4], splitted_line[5]]
            df_dict.update({splitted_line[2]: list_for_df})
        return pd.DataFrame.from_dict(df_dict, orient="index")


class _msr:
    def __init__(self, msr):
        self.msr = msr[1:-1]

    def getDF(self):
        df_dict = {}
        msr_list = []
        acc_list = []
        key = ""
        for line in self.msr:
            splitted_line = line.strip().split(";")
            if splitted_line[0] == "[MSR:RECORD]":
                key = splitted_line[2]
                msr_list = [splitted_line[4], splitted_line[5], splitted_line[8]]
                continue
            else:
                acc_list = splitted_line[2:]
            msr_list = msr_list + acc_list
            df_dict.update({key: msr_list})
            msr_list = []
            acc_list = []
            key = ""
        return pd.DataFrame.from_dict(df_dict, orient="index")


class _msrData:
    def __init__(self, msr_data):
        self.msr_data = msr_data[1:-1]

    def getDF(self):
        toggle = False
        df_dict = {}
        df_list = []
        key = ""
        typ = ""
        # Suchen nach Key wörtern in der Liste
        ld_bs = np.char.find(self.msr_data[1:-1], "[LAD:BSINST]")
        ld_ref = np.char.find(self.msr_data[1:-1], "[LAD:MSR_REF]")
        para_data = np.char.find(self.msr_data[1:-1], "[PARA:PARADATA]")
        for count, status in enumerate(ld_bs):
            if status != -1:
                typ = self.msr_data[count].strip().split(";")[3]
                toggle = True
            if toggle and ld_ref[count] != -1:
                key = self.msr_data[count].strip().split(";")[1]
                if para_data[count + 1] != -1:
                    df_list.append(typ)
                    para = self.msr_data[count + 1].strip().split(";")[1:]
                    df_list += para
                df_dict.update({key: df_list})
                df_list = []
                typ = ""
                key = ""
                toggle = False
        return pd.DataFrame.from_dict(df_dict, orient="index")

    def getFgr(self):
        self.search = [
            "[PBV:OBJPATH]",
            "FGRBLT",
            "Pool",
        ]
        fgr = []
        for row in self.msr_data:
            if (
                self.search[0] in row
                and self.search[1] in row
                and not self.search[2] in row
            ):
                splitted_row = row.strip().split(";")
                fgr.append(splitted_row[-1])
        fgr.sort()
        return pd.DataFrame(data=fgr)


class _hwm:
    def __init__(self, hwm):
        self.hwm = hwm

    def getDF(self):
        for i in self.hwm:
            if "[HW2_BLOB]" in i:
                continue
            if "[HW2_NODE]" in i:
                print(i)


class _eam:
    def __init__(self, eam):
        self.eam = eam[1:-1]

    def getDF(self):
        df_dict = {}
        for var in self.eam:
            splitted_var = var.strip().split(";")
            if len(splitted_var) > 2:
                df_dict.update({splitted_var[2]: [splitted_var[3]]})
        return pd.DataFrame.from_dict(df_dict, orient="index")


class Evaluation:
    status = 0

    def __init__(self, *args):
        if len(args) > 7:
            print("zuviel Daten Übergeben")
            self.status = 1
        else:
            self.project = _project(args[0])
            self.area = _area(args[1])
            self.var = _var(args[2])
            self.msr = _msr(args[3])
            self.msrData = _msrData(args[4])
            self.hwm = _hwm(args[5])
            self.eam = _eam(args[6])

    def __str__(self):
        return str(self.status)

    def getProjectDF(self):
        return self.project.getDF()

    def getAreaDF(self):
        return self.area.getDF()

    def getVarDF(self):
        return self.var.getDF()

    def getMsrDF(self):
        return self.msr.getDF()

    def getMsrDataDF(self):
        return self.msrData.getDF()

    def getGraficsDF(self):
        return self.msrData.getFgr()

    def getHwmDF(self):
        return self.hwm.getDF()

    def getEamDF(self):
        return self.eam.getDF()


from readFile import *
from parsingFreelance import *

# index zu einer liste mit dem befehl  .index.tolist()
filepath = "/Users/peterschwarz/VS Code Projekte/ParseClass/elektrolyse_20200326.csv"
input = WorkWithFile(read, filepath).execute()
parsed_data = Freelance(input).get_data()
test = Evaluation(*parsed_data)
print(test.getHwmDF())
print(test)

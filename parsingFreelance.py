from os import closerange
import pandas as pd
import numpy as np


class Section(object):
    df_data = []
    data = []
    fgr_row = []
    project = [0]
    area = [0, 0]
    var = [0, 0]
    msr = [0, 0]
    data_msr = [0, 0]
    hwm = [0, 0]
    eam = [0, 0]
    __key_worte = [
        "[BEGIN_PROJECTHEADER]",
        "[BEGIN_AREADEFINITION]",
        "[END_AREADEFINITION]",
        "[BEGIN_EAMSECTION]",
        "[END_EAMSECTION]",
        "[BEGIN_MSRSECTION]",
        "[END_MSRSECTION]",
        "[BEGIN_PBAUMSECTION]",
        "[END_PBAUMSECTION]",
        "[BEGIN_HARDWAREMANAGER]",
        "[END_HARDWAREMANAGER]",
        "[BEGIN_RESOURCEASSOCIATIONSECTION]",
        "[END_RESOURCEASSOCIATIONSECTION]",
        "[PBV:OBJPATH]",
        "FGRBLT",
        "Pool",
    ]

    def __init__(self, input, parsing=None):
        if parsing is None:
            self.parseFreelance(input)
        else:
            print("Auto parse Ausgeschaltet")

    def parseFreelance(self, input):
        print("Parse Ausgeführt")
        for count, row in enumerate(input):
            if self.__key_worte[0] in row:
                self.project[0] = count
            if self.__key_worte[1] in row:
                self.area[0] = count
            if self.__key_worte[2] in row:
                self.area[1] = count
            if self.__key_worte[3] in row:
                self.var[0] = count
            if self.__key_worte[4] in row:
                self.var[1] = count
            if self.__key_worte[5] in row:
                self.msr[0] = count
            if self.__key_worte[6] in row:
                self.msr[1] = count
            if self.__key_worte[7] in row:
                self.data_msr[0] = count
            if self.__key_worte[8] in row:
                self.data_msr[1] = count
            if self.__key_worte[9] in row:
                self.hwm[0] = count
            if self.__key_worte[10] in row:
                self.hwm[1] = count
            if self.__key_worte[11] in row:
                self.eam[0] = count
            if self.__key_worte[12] in row:
                self.eam[1] = count
            if (
                self.__key_worte[13] in row
                and self.__key_worte[14] in row
                and not self.__key_worte[15] in row
            ):
                self.fgr_row.append(count)
            self.data.append(row.strip().split(";"))

    def get_project(self):
        pass

    def get_areas(self):
        pass

    def get_data(self):
        self.get_project()
        self.get_areas()
        return self.df_data


class Freelance(Section):
    def __init__(self, input, parsing=None):
        if parsing is None:
            self.parseFreelance(input)
        else:
            print("Auto parse Ausgeschaltet")

    def get_project(self):
        df = pd.DataFrame(self.data[self.project[0]])
        self.df_data.append(df)

    def get_areas(self):
        df = pd.DataFrame(self.data[self.area[0] : self.area[1]])
        self.df_data.append(df)

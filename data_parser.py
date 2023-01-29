import pandas


class DataParsed:

    def __init__(self, celeb_name):
        self.data = pandas.read_csv("adb_people_data.csv")
        self.data_col_names = [col_name for col_name in self.data.to_dict().keys()]
        self.idx = self.data.index[self.data['public_data/sflname'] == celeb_name].tolist()[0]

        self.name = self.data.iloc[self.idx][1]
        self.dob = self.data.iloc[self.idx][4]
        self.hour = self.get_hour()
        self.minute = self.get_minute()
        self.city = self.data.iloc[self.idx][2]
        self.country = self.data.iloc[self.idx][3]

    def get_minute(self):
        minute = ""
        minute_idx = 0
        for char in self.data.iloc[self.idx][5]:
            if char == ":":
                minute_idx += 1
            elif minute_idx == 1:
                minute += char
        return minute

    def get_hour(self):
        hour = ""
        for char in self.data.iloc[self.idx][5]:
            if char == ":":
                break
            else:
                hour += char
        return hour


import kerykeion as kr
import svg_chart_custom as svg_custom


class User:

    def __init__(self, name, dob, hour, minute, city, country):
        self.name = name
        self.dob = dob
        self.hour = hour
        self.minute = minute
        self.city = city
        self.country = country
        self.astro_data = kr.KrInstance(self.name, int(self.parse_year()), int(self.parse_month()),
                                        int(self.parse_day()), int(self.hour), int(self.minute),
                                        self.city, self.country)
        self.chart = svg_custom.MakeSvgInstancePlacidus(self.astro_data, chart_type="Natal")
        self.report = kr.Report(self.astro_data)

    def print_svg_chart(self):
        self.chart.makeSVG()

    def print_all_data(self):
        kr.print_all_data(self.astro_data)


    def parse_month(self):
        month = ""
        for char in self.dob:
            if char == "/":
                break
            else:
                month += char
        return int(month)

    def parse_day(self):
        day = ""
        day_idx = 0
        for char in self.dob:
            if char == "/":
                day_idx += 1
            elif day_idx == 1:
                day += char
            elif day_idx == 2:
                break
        return int(day)

    def parse_year(self):
        year = ""
        year_idx = 0
        for char in self.dob:
            if char == "/":
                year_idx += 1
            elif year_idx == 2:
                year += char
        return int(year)

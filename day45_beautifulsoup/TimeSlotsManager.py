from bs4 import BeautifulSoup
from datetime import datetime

NAME = "div"
CLASS_T ="margin-left: 6px; margin-right: 2px;"
CLASS_D ="italki-row flex flex-row"
TIME_SLOTS_MIDDLE_RAW = "margin-left: 6px; margin-right: 2px;"
TIME_SLOTS_FIRST_RAW = TIME_SLOTS_MIDDLE_RAW
TIME_SLOTS_LAST_RAW = TIME_SLOTS_MIDDLE_RAW

class TimeGrab:
    def __init__(self,file):
        '''the content should be the file encoded by utf-8 and should be read from an html file'''
        self.content = self.read_file(file)
        self.soup = BeautifulSoup(self.content,"html.parser")
        self.times_tag_list = self.soup.find_all(name="div", style=CLASS_T)
        self.dates_tag_list = self.soup.find_all(name="div", class_=CLASS_D)
        self.dates = [content.getText() for date in self.dates_tag_list for content in date.contents]
        self.time_slots = [time.getText() for time in self.times_tag_list]
        self.indices = self.find_critical_indices(self.dates)
        self.time_slots_first = []
        self.time_slots_last = []
        self.time_slots_all = []
        self.delta_total = 0
        self.lesson_1h = 0
        self.lesson_30min = 0
        self.lesson_45min = 0
        self.iterate()
        self.calculate_time()
        self.get_report()
        print(self.time_slots_all)
    def find_critical_indices(self,dates) -> list:
        indices = [dates.index(date) for date in dates if self.check_letter(date)]

        return indices

    def check_letter(self,date):
        for char in date:
            if char.isalpha():
                return True
    def read_file(self,file):
        with open(file,encoding='utf-8') as data:
            content = data.read()

            return content

    def iterate(self):
        soup_str = ""
        rows_raw_list = self.soup.find(name="div", class_="italki-month-content").contents
        ################FROM LINE TWO TO THE LAST BUT ONE LINE################################




        try:
            if self.indices[1] % 7 != 0:
                for row in rows_raw_list[1:int(self.indices[1]/7)]:
                    soup_str += str(row)
                row_soup_m =  BeautifulSoup(soup_str,"html.parser")
                time_slots_middle_raw = row_soup_m.find_all(name="div", style=TIME_SLOTS_MIDDLE_RAW)
                time_slots_middle = [time_slot.getText() for time_slot in time_slots_middle_raw]

            else:
                for row in rows_raw_list[1:int(self.indices[1]/7)-1]:
                    soup_str += str(row)
                row_soup_m =  BeautifulSoup(soup_str,"html.parser")
                time_slots_middle_raw = row_soup_m.find_all(name="div", style=TIME_SLOTS_MIDDLE_RAW)
                time_slots_middle = [time_slot.getText() for time_slot in time_slots_middle_raw]

        except IndexError:

            for row in rows_raw_list[1:]:
                soup_str += str(row)
            row_soup_m = BeautifulSoup(soup_str, "html.parser")
            time_slots_middle_raw = row_soup_m.find_all(name="div", style= TIME_SLOTS_MIDDLE_RAW)
            time_slots_middle = [time_slot.getText() for time_slot in time_slots_middle_raw]





        #############################first row##############################################################
        first_row_raw = rows_raw_list[0]
        row_soup_first = BeautifulSoup(str(first_row_raw),"html.parser")
        first_row_lines = row_soup_first.find_all(name = "div",class_="italki-row flex")
        # for line in first_row_lines:
        #     line_soup = BeautifulSoup(str(line), "html.parser")
        #     segments_line = line_soup.find_all(name="div", class_="text-tiny font-medium text-gray3 mr-1")

            # for segment in segments_line[self.indices[0]:]:
        for line in first_row_lines:
            line_soup = BeautifulSoup(str(line), "html.parser")
            line_segments = line_soup.find_all(name="div", class_="italki-row-segment")
            for segment in line_segments:
                try:
                    if segment["style"] != "flex-basis: 14.2857%; max-width: 14.2857%;":
                        reference_num = [sub for sub in segment["style"].split("%;")][0].split()[1]
                        multiply_by = round(float(reference_num) / 14.2857)

                        segment["style"] = "flex-basis: 14.2857%; max-width: 14.2857%;"
                        ######################for 28% (接下来要想想怎么根据倍数插入相应的数量的item#################################

                        num_added = multiply_by - 1
                        for _ in range(num_added):
                            line_segments.insert(line_segments.index(segment), "placeholder")
                except TypeError:
                    pass

            for segment in line_segments[self.indices[0]:]:
                segment_soup = BeautifulSoup(str(segment), "html.parser")

                segment_slot = segment_soup.find(name="div", style= TIME_SLOTS_FIRST_RAW)

                try:
                    self.time_slots_first.append(segment_slot.getText())
                except AttributeError:
                    self.time_slots_first = self.time_slots_first

        #######################last row#############################################################
        last_row_raw = rows_raw_list[-1]
        row_soup_last = BeautifulSoup(str(last_row_raw), "html.parser")
        last_row_lines = row_soup_last.find_all(name="div", class_="italki-row flex")

        for line in last_row_lines:
            line_soup_l = BeautifulSoup(str(line), "html.parser")
            line_segments_l = line_soup_l.find_all(name="div", class_="italki-row-segment")

            for segment in line_segments_l:
                try:
                    if segment["style"] != "flex-basis: 14.2857%; max-width: 14.2857%;":
                        reference_num = [sub for sub in segment["style"].split("%;")][0].split()[1]
                        multiply_by = round(float(reference_num) / 14.2857)

                        segment["style"] = "flex-basis: 14.2857%; max-width: 14.2857%;"
                        ######################for 28% (接下来要想想怎么根据倍数插入相应的数量的item#################################

                        num_added = multiply_by - 1
                        for _ in range(num_added):
                            line_segments_l.insert(line_segments_l.index(segment), "placeholder")
                except TypeError:
                    pass

            try:
                for segment in line_segments_l[:self.indices[1] % 7]:
                    segment_soup_l = BeautifulSoup(str(segment), "html.parser")
                    segment_slot_l = segment_soup_l.find(name="div", style=TIME_SLOTS_LAST_RAW)
                    try:
                        self.time_slots_last.append(segment_slot_l.getText())
                    except:
                        self.time_slots_last = self.time_slots_last

            except IndexError:
                self.time_slots_last = []

        self.time_slots_all = self.time_slots_first + time_slots_middle + self.time_slots_last

    def calculate_time(self):

        for time_slot in self.time_slots_all:
            end_time = [char for char in time_slot[6:11]]
            start_time = [char for char in time_slot[0:5]]
            end_time_str = ""
            start_time_str = ""
            for char in start_time:
                start_time_str += char
            for char in end_time:
                end_time_str += char

            start_time_dt = datetime.strptime(start_time_str, "%H:%M")
            end_time_str_dt = datetime.strptime(end_time_str, "%H:%M")
            delta = end_time_str_dt - start_time_dt

            self.delta_total += delta.total_seconds() / 3600

            if delta.total_seconds() == 1800:
                self.lesson_30min += 1
            elif delta.total_seconds() == 2700:
                self.lesson_45min += 1
            elif delta.total_seconds() == 3600:
                self.lesson_1h += 1


    def get_report(self):
        print(f"You have taught {self.lesson_1h + self.lesson_30min + self.lesson_45min} lessons in {self.dates[self.indices[0]].split()[0]}.!(p≧w≦q)\nYou have spent {self.delta_total} hours on italki this month!٩(๑>◡<๑)۶\nYou have taught {self.lesson_1h} 1h lessons this month.\nYou have taught {self.lesson_45min} 45min lessons this month.\nYou have taught {self.lesson_30min} 30min lessons this month.")



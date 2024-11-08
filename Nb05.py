import random
import copy

s_rank_list = [1, 2, 3, 4, 5]
c_rank_list = [1, 2, 3, 4, 5, 6, 7] # 高い順

class Student:
    def __init__(self, id, s_type):
        self.id = id
        self.rank = s_rank_list[(id) % len(s_rank_list)]
        self.offers = [] # 内定先
        self.s_type = s_type
        if s_type == "normal":
            self.start_day = 180
            self.cycle = 30

    def __str__(self):
        return f"id: {self.id}, rank: {self.rank}"

    def update(self, day, recruiting_c):
        if day >= self.start_day and (day - self.start_day) % self.cycle == 0:
            self.apply(recruiting_c)

    def apply(self, num_companies, s_to_c):

        return
            

class Company:
    def __init__(self, id, c_positions):
        self.id = id
        self.rank = c_rank_list[(id-1) % len(c_rank_list)]
        self.naitei_member = [] # 内定者
        self.positions = c_positions

def Simulation():
    num_students = 600
    num_companies = 21
    c_positions = 50
    day = 0
    students = []
    companies = []

    # -- 初期化 --
    for s in range(num_students):
        students.append(Student(s, "normal"))
    for c in range(num_companies):
        companies.append(Company(c, c_positions))
    
    # for student in students:
    #     print(str(student))
    
    # idで募集中の企業を管理
    recruiting_c = list(range(num_companies))
    # print(recruiting_c)
    
    s_to_c = {} # 応募管理リスト

    # s_to_c = {"学生id": ["企業のid", "企業のid", "企業のid"], ...}
    # 応募
    for student in students:
        s_to_c[student.id] = []# random3つ

    limit = True
    while limit:
        print("ss")

if __name__ == "__main__":
    Simulation()

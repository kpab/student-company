import numpy as np
import matplotlib.pyplot as plt
import random


# シミュレーションパラメータの設定
num_students = 6  # 学生の総数
student_ranks = ['A', 'B', 'C', 'D', 'E']  # 学生のランク
students_per_rank = num_students // len(student_ranks)  # 各ランクごとの学生数


num_companies = 21 # 企業の総数
company_ranks = ['S', 'A', 'B', 'C', 'D', 'E', 'F']  # 企業のランク
companies_per_rank = num_companies // len(company_ranks)  # 各ランクの企業数
positions_per_company = 50  # 企業ごとの採用枠


days_in_simulation = 720 # シミュレーションの期間（日数）
num_simulations = 1  # シミュレーション回数


# 採用確率を設定
offer_probabilities = {
    'lower': 0.9,  # 自分のランクより低い企業からの内定確率
    'equal': 0.6,  # 同じランクの企業からの内定確率
    'higher': 0.1  # 自分のランクより高い企業からの内定確率
}


# 学生と企業ランクに応じた点数を定義(グラフ用)
rank_scores = {
    'S': 7, 'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1
}


# 学生と企業ランクに対応する数値を定義（比較用）
rank_values = {
    'S': 7, 'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1
}






class Student:
    def __init__(self, id, rank, application_start_day, offers, applications_per_cycle, application_cycle):
        self.id = id  # 学生のID
        self.rank = rank  # 学生のランク
        self.application_start_day = application_start_day  # 応募開始日
        self.offers = offers  # 受けた内定のリスト
        self.applications_per_cycle = applications_per_cycle  # サイクルごとの応募数
        self.application_cycle = application_cycle  # 応募サイクルの期間
        self.has_job = False  # 内定を持っているかどうか
        self.job_rank = None  # 最終的に内定を受けた企業のランク
        self.total_applications = 0  # 応募した企業の総数


    def apply_to_company(self, companies, day):
        # 応募サイクルに基づいて応募を開始する日かどうかを確認
        if day >= self.application_start_day and (day - self.application_start_day) % self.application_cycle == 0:
            available_companies = [company for company in companies]
            selected_companies = []


            # 応募可能な企業数がapplications_per_cycleに満たない場合、最大限応募
            while len(selected_companies) < self.applications_per_cycle and available_companies:
                company = random.choice(available_companies)
                selected_companies.append(company)
                available_companies.remove(company)  # 同じ企業に重複して応募しないように削除
            
            # 応募処理
            company_info = []
            for company in selected_companies:
                company.process_application(self)  # 各企業に応募を処理
                company_info.append(f"Company ID {company.id} (Rank {company.rank})")
                self.total_applications += 1


            #🌟🌟🌟🌟🌟🌟 応募状況を表示
            #print(f"Student ID {self.id} (Rank {self.rank}) applied to: {', '.join(company_info)}")








    def decide_offer(self):
        if self.offers:  # 受け取った内定がある場合に以下の処理を行う。受けた内定のリストが空でない場合
            highest_rank = max(rank_values[offer.rank] for offer in self.offers)
            highest_offers = [offer for offer in self.offers if rank_values[offer.rank] == highest_rank]
            # 最高ランクの企業が複数ある場合、ランダムに一つ選ぶ
            highest_offer = random.choice(highest_offers)


            if rank_values[highest_offer.rank] >= rank_values[self.rank]:
                self.has_job = True  # 内定を受けた
                self.job_rank = highest_offer.rank  # 受けた企業のランク
                return highest_offer


            if not self.has_job:
                return "Continue applying"  # 内定がない場合は応募を続ける


        return None
    
    def __repr__(self):
        return (f"student_Agent(id={self.id},  "
                f"has_job={self.has_job},"
                f"job_rank={self.job_rank},"
                f"rank={self.rank}")
    
                















class Company:
    def __init__(self, id,rank, positions):
        self.id = id  # 企業のID
        self.rank = rank  # 企業のランク
        self.positions = positions  # 採用枠
        self.applicants = []  # 応募者のリスト




    def apply(self, student):
        self.applicants.append(student)  # 学生を応募者リストに追加


    def make_hiring_decisions(self, students):
        """応募者に対して採用判断を行う。"""
        self.process_applications()  # 応募者リストを処理


    def process_applications(self):
        """30日サイクルで応募者をランダムに処理し、内定を出すか判断する。"""
    # 応募者リストをランダムに並べ替え
        random.shuffle(self.applicants)


    # 並べ替えた応募者を処理して内定を出す
        for student in self.applicants:
            
            if self.positions > 0:  # 採用枠が残っている場合のみ処理
                self.process_application(student)


    # 応募者リストをクリア
        self.applicants.clear()




    def process_application(self, student):
        """個別の応募を処理し、内定を出すか判断する。"""
    # 学生のランクに応じた内定確率を決定
        if rank_values[self.rank] > rank_values[student.rank]:
            prob = offer_probabilities['higher']
        elif rank_values[self.rank] == rank_values[student.rank]:
            prob = offer_probabilities['equal']
        else:
            prob = offer_probabilities['lower']


    # 内定を出す確率に基づいて学生を採用
        if np.random.rand() < prob:
            self.hire_student(student)  # 学生を採用




    def hire_student(self, student):
        """学生を採用する処理。"""
        if self.positions > 0:  # 採用枠がある場合
        # 採用枠を highest_offer の数だけ減らす
            highest_offer_count = sum(1 for offer in student.offers if offer == self)
            self.positions -= min(self.positions, highest_offer_count)  # 採用枠が負にならないよう調整


            student.has_job = True  # 学生が内定を受けたことを記録
            student.offers.append(self)  # 学生に内定を追加
            return True
        return False


    def update_positions(self):
        """企業の採用枠を更新する処理。"""
    # 必要に応じて追加のロジックを実装
        pass  # 採用枠の更新が必要な場合に実装
    def __repr__(self):
        return (f"company_Agent(id={self.id},  "
                f"oubo={self.applicants},"
                f"rank={self.rank}")
        
        
        
   






# 学生と企業の初期化
def initialize_students():
    students = []
    id_counter = 1  # IDのカウンターを初期化
    for rank in student_ranks:
        for _ in range(students_per_rank):
            # 各学生を初期化し、IDを割り当てる
            students.append(Student(id=id_counter, rank=rank, application_start_day=180, offers=[], applications_per_cycle=3, application_cycle=30))
            id_counter += 1  # IDをインクリメント
    return students




def initialize_companies():
    companies = []
    id_counter = 1
    for rank in company_ranks:
        for _ in range(companies_per_rank):
            companies.append(Company(id=id_counter, rank=rank, positions=positions_per_company))
            id_counter += 1
    return companies
















def run_simulation(companies):
    students = initialize_students()  # 学生を初期化
    score_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 得点の統計
    offer_rates = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 内定率の統計
    applications_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 応募統計






    # シミュレーションの各日を表し、シミュレーションが行われる期間
    for day in range(180,days_in_simulation):
        # 学生が企業に応募
        for student in students:
            student.apply_to_company(companies, day)  # 企業に応募



        # 企業が採用確率に基づいて学生に対して採用判断
        for company in companies:
            company.make_hiring_decisions(students)  # 企業による採用判断のメソッドを呼び出す


        #  学生が自分のランク以上の企業からの内定のみ、内定と判断→内定を受け取る
        for student in students:
            student.decide_offer()  # 学生が内定を決定する


        # 内定を受け取った学生分、採用枠減らす
        for company in companies:
            company.update_positions()  # 採用枠を減らすメソッドを呼び出す
# =============================================================================
#         for da in range(30):
#             print("シミュレーション切り替わり")
# =============================================================================
        print("シミュ切り替わり")
        for student in students:
            if student.rank=='B':
                print(day)
                print(student)


     
       # 🌟🌟🌟内定スコアと内定率の計算
        for rank in student_ranks:
            
            score_today = sum(rank_scores.get(s.job_rank, 0) for s in students
        if s.has_job and s.rank == rank and s.job_rank is not None and s.job_rank >= s.rank)
            """score_today = sum(rank_scores.get(s.job_rank, 0) for s in students if s.has_job and s.rank == rank)"""
            score_stats[rank][day] = score_today / students_per_rank  # 平均得点を計算
                
                # 内定率を計算
            offer_today = sum( 1 for s in students if s.has_job and s.rank == rank and s.job_rank is not None and s.job_rank >= s.rank)
            """offer_today = sum(1 for s in students if s.has_job and s.rank == rank)"""
            offer_rates[rank][day] = offer_today / students_per_rank  # 内定率を計算


  


         # 応募数を計算
            applications_today = sum(s.total_applications for s in students if s.rank == rank)
            applications_stats[rank][day] = applications_today / students_per_rank  # 平均応募数を計算

# =============================================================================
#     for company in companies:
#         print(company)
# 
# =============================================================================





    return score_stats, offer_rates, applications_stats  # 統計を返す








   


# 複数回のシミュレーションを実行
def run_multiple_simulations(num_simulations):
    all_simulations_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションの得点統計
    all_offer_rates = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションの内定率統計
    all_applications_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションの応募統計


    for _ in range(num_simulations):
        companies = initialize_companies()  # 企業を初期化
        score_stats, offer_rates, applications_stats = run_simulation(companies)  # シミュレーションを実行
        
        for rank in student_ranks:
            all_simulations_stats[rank] += score_stats[rank]  # 統計を加算
            all_offer_rates[rank] += offer_rates[rank]
            all_applications_stats[rank] += applications_stats[rank]


    # 平均を計算
    for rank in student_ranks:
        all_simulations_stats[rank] /= num_simulations
        all_offer_rates[rank] /= num_simulations
        all_applications_stats[rank] /= num_simulations


    return all_simulations_stats, all_offer_rates, all_applications_stats  # 統計を返す


# シミュレーションの実行
score_stats, offer_rates, applications_stats = run_multiple_simulations(num_simulations)










'''
#🌟🌟🌟🌟🌟🌟
print("学生のIDとランク:")
for student in initialize_students():  # 学生の初期化を再度呼び出す
    print(f"ID: {student.id}, Rank: {student.rank}")
    




# 企業のIDとランクを出力
print("企業のIDとランク:")
for company in initialize_companies():
    print(f"ID: {company.id}, Rank: {company.rank}")
    
    
'''   
    




# グラフ描画
def plot_results(score_stats, offer_rates, applications_stats):
    plt.figure(figsize=(15, 10))


    # 得点のグラフ
    plt.subplot(3, 1, 1)
    for rank in student_ranks:
        plt.plot(score_stats[rank], label=f'{rank} Rank Score',linewidth=2.8)
    plt.title('Average Scores Over Time')
    plt.xlabel('Days')
    plt.ylabel('Average Score')
    plt.legend()


    # 内定率のグラフ
    plt.subplot(3, 1, 2)
    for rank in student_ranks:
        plt.plot(offer_rates[rank], label=f'{rank} Rank Offer Rate',linewidth=2.8)
    plt.title('Offer Rates Over Time')
    plt.xlabel('Days')
    plt.ylabel('Offer Rate')
    plt.legend()


    # 応募数のグラフ
    plt.subplot(3, 1, 3)
    for rank in student_ranks:
        plt.plot(applications_stats[rank], label=f'{rank} Rank Applications')
    plt.title('Application Rates Over Time')
    plt.xlabel('Days')
    plt.ylabel('Application Rate')
    plt.legend()


    plt.tight_layout()
    plt.show()


# グラフを描画
plot_results(score_stats, offer_rates, applications_stats)
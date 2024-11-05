# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:16:24 2024

@author: AYAKA
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:40:48 2024

@author: AYAKA
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# シミュレーションパラメータの設定
num_students = 600  # 学生の総数
student_ranks = ['A', 'B', 'C', 'D', 'E']  # 学生のランク
students_per_rank = num_students // len(student_ranks)  # 各ランクごとの学生数

num_companies = 21  # 企業の総数
company_ranks = ['S', 'A', 'B', 'C', 'D', 'E', 'F']  # 企業のランク
companies_per_rank = num_companies // len(company_ranks)  # 各ランクの企業数
positions_per_company = 50  # 企業ごとの採用枠

days_in_simulation = 720  # シミュレーションの期間（日数）
num_simulations = 2  # シミュレーション回数

# 採用確率を設定
offer_probabilities = {
    'lower': 0.9,  # 自分のランクより低い企業からの内定確率
    'equal': 0.6,  # 同じランクの企業からの内定確率
    'higher': 0.1  # 自分のランクより高い企業からの内定確率
}

# 学生と企業ランクに応じた点数を定義
rank_scores = {
    'S': 7, 'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1
}

# 学生と企業ランクに対応する数値を定義（比較用）
rank_values = {
    'S': 7, 'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1
}

# 学生クラスの定義
class Student:
    def __init__(self, rank, application_start_day, offers, applications_per_cycle, application_cycle):
        self.rank = rank  # 学生のランク
        self.application_start_day = application_start_day  # 応募開始日
        self.offers = offers  # 受けた内定のリスト
        self.applications_per_cycle = applications_per_cycle  # サイクルあたりの応募数
        self.application_cycle = application_cycle  # 応募サイクルの日数
        self.has_job = False  # 内定を持っているかどうか
        self.job_rank = None  # 最終的に内定を受けた企業のランク
        self.total_applications = 0  # 応募した企業の総数

    def apply_to_company(self, companies, day):
        # 応募サイクルに基づいて応募を開始する日かどうかを確認
        if day >= self.application_start_day and (day - self.application_start_day) % self.application_cycle == 0:
            selected_companies = random.sample(companies, min(self.applications_per_cycle, len(companies)))  # 応募する企業をランダムに選択
            for company in selected_companies:
                company.process_application(self)  # 企業に応募を処理してもらう
                self.total_applications += 1  # 応募数をカウント

    def decide_offer(self):
        # 受けた内定がある場合、最も高いランクの企業からの内定を選択
        if self.offers:
            highest_offer = max(self.offers, key=lambda c: rank_values[c.rank])  # 最も高いランクの企業を選ぶ
            if rank_values[highest_offer.rank] >= rank_values[self.rank]:  # 内定の企業が学生のランク以上の場合
                self.has_job = True  # 内定を持っていると設定
                self.job_rank = highest_offer.rank  # 内定を受けた企業のランクを設定
                for offer in self.offers:  # 他の内定を辞退する処理
                    if offer != highest_offer:
                        offer.positions += 1  # 企業の採用枠を増やす
                return highest_offer  # 選択した内定を返す
        if not self.has_job:  # 内定がない場合は、引き続き応募
            return "Continue applying"
        return None

# 企業クラスの定義
class Company:
    def __init__(self, rank, positions):
        self.rank = rank  # 企業のランク
        self.positions = positions  # 採用枠

    def process_application(self, student):
        # 学生のランクに応じて内定の確率を決定
        if rank_values[self.rank] > rank_values[student.rank]:
            prob = offer_probabilities['higher']
        elif rank_values[self.rank] == rank_values[student.rank]:
            prob = offer_probabilities['equal']
        else:
            prob = offer_probabilities['lower']
        
        if np.random.rand() < prob:  # 確率に基づいて内定を出すか判断
            self.hire_student(student)

    def hire_student(self, student):
        # 採用枠が残っている場合に学生を採用
        if self.positions > 0:
            self.positions -= 1  # 採用枠を1減らす
            student.offers.append(self)  # 学生の内定リストに追加
            return True
        return False

# 学生の初期化
def initialize_students():
    students = []
    for rank in student_ranks:
        for _ in range(students_per_rank):
            students.append(Student(rank, application_start_day=180, offers=[], applications_per_cycle=3, application_cycle=30))
    return students

# 企業の初期化
def initialize_companies():
    companies = []
    for rank in company_ranks:
        companies += [Company(rank, positions_per_company) for _ in range(companies_per_rank)]  # 各企業の初期化
    return companies

# シミュレーションを実行し、内定状況を記録
def run_simulation(companies):
    students = initialize_students()  # 学生の初期化
    score_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 学生ランクごとのスコア記録
    offer_rates = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 学生ランクごとの内定率記録
    applications_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 学生ランクごとの応募数記録

    for day in range(days_in_simulation):  # 日数のループ
        for student in students:
            student.apply_to_company(companies, day)  # 企業に応募
            student.decide_offer()  # 内定の決定

        # 学生ランクごとの統計を更新
        for rank in student_ranks:
            score_today = sum(rank_scores.get(s.job_rank, 0) for s in students if s.has_job and s.rank == rank)  # 当日のスコアを計算
            score_stats[rank][day] = score_today / students_per_rank  # 平均スコアを記録
            offer_count = sum(1 for s in students if s.has_job and s.rank == rank)  # 内定を受けた学生の数
            offer_rates[rank][day] = offer_count / students_per_rank  # 内定率を記録
            applications_count = sum(s.total_applications for s in students if s.rank == rank)  # 応募数を計算
            applications_stats[rank][day] = applications_count / students_per_rank  # 平均応募数を記録

    return score_stats, offer_rates, applications_stats  # 結果を返す

# 複数回のシミュレーションを実行
def run_multiple_simulations(num_simulations):
    all_simulations_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションのスコア
    all_offer_rates = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションの内定率
    all_applications_stats = {rank: np.zeros(days_in_simulation) for rank in student_ranks}  # 全シミュレーションの応募数

    for _ in range(num_simulations):
        companies = initialize_companies()  # 企業の初期化
        score_stats, offer_rates, applications_stats = run_simulation(companies)  # シミュレーション実行
        
        # 統計を合計
        for rank in student_ranks:
            all_simulations_stats[rank] += score_stats[rank]
            all_offer_rates[rank] += offer_rates[rank]
            all_applications_stats[rank] += applications_stats[rank]

    # 平均を計算
    for rank in student_ranks:
        all_simulations_stats[rank] /= num_simulations
        all_offer_rates[rank] /= num_simulations
        all_applications_stats[rank] /= num_simulations

    return all_simulations_stats, all_offer_rates, all_applications_stats  # 結果を返す

# 結果のプロット
def plot_results(all_simulations_stats, all_offer_rates, all_applications_stats):
    plt.figure(figsize=(10, 15))  # グラフのサイズを設定
    # スコアのプロット
    plt.subplot(3, 1, 1)
    for rank in student_ranks:
        plt.plot(all_simulations_stats[rank], label=f'Students of Rank {rank}')
    plt.title('Average Score Over Time')  # タイトル
    plt.xlabel('Days')  # x軸ラベル
    plt.ylabel('Average Score')  # y軸ラベル
    plt.legend()

    # 内定率のプロット
    plt.subplot(3, 1, 2)
    for rank in student_ranks:
        plt.plot(all_offer_rates[rank], label=f'Offer Rate for Rank {rank}')
    plt.title('Average Offer Rate Over Time')  # タイトル
    plt.xlabel('Days')  # x軸ラベル
    plt.ylabel('Offer Rate')  # y軸ラベル
    plt.legend()

    # 応募数のプロット
    plt.subplot(3, 1, 3)
    for rank in student_ranks:
        plt.plot(all_applications_stats[rank], label=f'Applications Count for Rank {rank}')
    plt.title('Average Applications Count Over Time')  # タイトル
    plt.xlabel('Days')  # x軸ラベル
    plt.ylabel('Average Applications Count')  # y軸ラベル
    plt.legend()

    plt.tight_layout()  # レイアウト調整
    plt.show()  # グラフを表示

# メイン処理
if __name__ == "__main__":
    all_simulations_stats, all_offer_rates, all_applications_stats = run_multiple_simulations(num_simulations)  # シミュレーション実行
    plot_results(all_simulations_stats, all_offer_rates, all_applications_stats)  # 結果をプロット

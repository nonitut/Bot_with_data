import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# def get_goal(user_id):
#     cursor.execute('''
#     SELECT goal
#     FROM profiles
#     WHERE user_id = ?
#     ''', (user_id,))
    
#     goal = cursor.fetchone()[0]
#     return goal


def get_user_notes(user_id):
    cursor.execute('''
        SELECT feels, money, date 
        FROM tablica
        WHERE user_id = ?
    ''', (user_id,))
    
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['feels','money','date'])
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
    return df


def plot_user_notes(notes_df):
    # if goal == "Жиросжигание":
    #     notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] + notes_df['expenses'])
    # elif goal == "Набор массы":
    #     notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] - notes_df['weight'] + 10)
    # elif goal == "Поддержание формы":
    #     notes_df['productivity'] = notes_df['wellbeing'] / (notes_df['weight'] + 10 - notes_df['weight'])
    # else:
    #     notes_df['productivity'] = notes_df['wellbeing']


    plt.style.use('seaborn-v0_8-darkgrid')
    plots = {}
    
    # График самочувствия
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['date'], notes_df['feels'], color='tab:red', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Самочувствие')
    ax.set_title('Зависимость самочувствия от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['feels'] = img_bytes
    plt.close(fig)

    # График веса
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(notes_df['date'], notes_df['money'], color='tab:blue', marker='o')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Деньги')
    ax.set_title('Зависимость трат от даты')
    ax.grid(True)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plots['money'] = img_bytes
    plt.close(fig)

    # # График затрат
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.plot(notes_df['created_at'], notes_df['expenses'], color='tab:green', marker='o')
    # ax.set_xlabel('Дата')
    # ax.set_ylabel('Затраты')
    # ax.set_title('Зависимость затрат от даты')
    # ax.grid(True)
    # img_bytes = BytesIO()
    # plt.savefig(img_bytes, format='png')
    # img_bytes.seek(0)
    # plots['expenses'] = img_bytes
    # plt.close(fig)

    # График продуктивности
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.plot(notes_df['created_at'], notes_df['productivity'], color='tab:purple', marker='o')
    # ax.set_xlabel('Дата')
    # ax.set_ylabel('Продуктивность')
    # ax.set_title('Зависимость продуктивности от даты')
    # ax.grid(True)
    # img_bytes = BytesIO()
    # plt.savefig(img_bytes, format='png')
    # img_bytes.seek(0)
    # plots['productivity'] = img_bytes
    # plt.close(fig)

    return plots
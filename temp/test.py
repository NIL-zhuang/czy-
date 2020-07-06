import json
import random
import urllib
from math import sqrt
import numpy as np

import DataUtils
from StudentGroup import getQuestionGroup, getStudentGroup
from evaluator import ScoreEvaluator
from temp.CaseData import CaseData

raw_case_map = {}  # 未处理的数据，map，键为case_id，内容为CaseData
case_student_map = {}  # 题目-学生列表
student_case_map = {}  # 学生-题目列表
student_ability = {}  # 学生能力值
case_difficulty = {}  # 题目难度
alpha = 1.15  # 运行时间权重
beta = 1.05  # 代码行数权重


# 算一次，然后存到json里，要不太浪费时间了
def score_evaluator_get_score_save(group):
    """
    :param group: 分组
    :return: 讲组内数据写入res.json中
    """
    init_map(group)
    out = open('res.json', 'w')
    res_map = {}
    f = open('C:\\Users\\NIL\\Documents\\GitHub\\NJU-basic-data-science\\test_data.json', encoding='utf-8')
    # f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\sample.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # for student in data:
    try:
        for student in student_case_map.keys():

            print('----------------student:',student,'处理开始------------------------')
            res_map[student] = {}
            cases = data[student]['cases']
            for case in cases:
                case_id = case['case_id']
                if len(case['upload_records']) == 0:
                    continue
                    # 不知道为什么会有空的提交记录...直接跳过叭 不然下面IndexError了
                url = case['upload_records'][-1]['code_url']
                res = ScoreEvaluator.getScore(url)
                print('正在处理 student=', student, ',case_id=', case_id)
                print(res)
                if res[2] == 'TIMEOUT':
                    print('timeout', student, case_id)
                res_map[student][case_id] = res

            print('----------------student:',student,'处理结束------------------------')
        out.write(json.dumps(res_map))
        f.close()
        out.close()
    except urllib.error.URLError:
        print('出现异常')
        out.write(json.dumps(res_map))
        f.close()
        out.close()


def mock_getScore(url):
    return True, 1, random.random(), random.random()


# 初始化四个map
def init_map(index):
    question_list = getQuestionGroup(index)
    student_list = getStudentGroup(index)
    for question in question_list:
        case_difficulty[question] = 1  # 初始默认难度为1
        case_student_map[question] = {}
        for student in student_list:
            case_student_map[question][student] = None
    for student in student_list:
        student_ability[student] = None
        student_case_map[student] = {}
        for question in question_list:
            student_case_map[student][question] = None


# 数据预处理
def pre_deal_data():
    for case_id in raw_case_map.keys():
        timeList = []
        lineList = []
        for raw_case in raw_case_map[case_id]:
            # print(raw_case)
            timeList.append(raw_case.time)
            lineList.append(raw_case.line)
        # print(timeList)
        timeAVG = np.average(timeList)
        timeVAR = np.var(timeList)
        lineAVG = np.average(lineList)
        lineVAR = np.var(lineList)
        for raw_case in raw_case_map[case_id]:
            temp = raw_case.copy()
            # TODO:缺省值处理加在这里，temp是新的对象
            time = DataUtils.omega(raw_case.time, timeAVG, timeVAR)
            line = DataUtils.omega(raw_case.line, lineAVG, lineVAR)
            temp.score = temp.score * alpha * time * beta * line
            student_case_map[temp.user_id][temp.case_id] = temp
            case_student_map[temp.case_id][temp.user_id] = temp
            print(temp)


# 数据读取
def read_data():
    f = open('test_data.json', encoding='utf-8')
    # f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\sample.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # for student in data:
    for student in student_case_map.keys():
        cases = data[student]['cases']
        for case in cases:
            case_id = case['case_id']
            if len(case['upload_records']) == 0:
                continue
                # 不知道为什么会有空的提交记录...直接跳过叭 不然下面IndexError了
            raw_score = case['upload_records'][-1]['score']
            url = case['upload_records'][-1]['code_url']
            res = ScoreEvaluator.getScore(url)
            print(res)
            # res = mock_getScore(url)
            if res[0]:  # 如果不是异常提交，才加入
                if case_id not in raw_case_map.keys():
                    raw_case_map[case_id] = []
                temp = CaseData(case_id, student, url, raw_score * res[1], res[2], res[3])
                # print(temp)
                raw_case_map[case_id].append(temp)
            student_case_map[student][case_id] = temp
            case_student_map[case_id][student] = temp
    print(raw_case_map)

    f.close()


# 迭代计算
# times: 迭代轮次
def calculate(times):
    for i in range(times):
        # 计算Bi
        for s in student_ability.keys():  # 对每个学生
            temp_ability = 0
            count = 0  # 有效数据的个数
            for q in case_difficulty.keys():  # 遍历每个题目
                if student_case_map[s][q] is not None:
                    temp_ability += case_difficulty[q] * student_case_map[s][q].score
                    count += 1
            # 这里有两种处理方法，一种是没做的题目也算在n里（即看为0分），一种是不算在n里，不知道取用哪一种
            temp_ability /= len(case_difficulty.keys())
            # temp_ability /= count
            student_ability[s] = temp_ability
        # 计算Qi
        b = 1  # 反正是个常数，当1处理，有需要再修改这里
        array = []
        for value in student_ability.values():
            array.append(value)
        B_AVG = np.average(array)
        B_VAR = np.var(array)
        for q in case_difficulty.keys():
            temp = 0
            count = 0
            for s in student_ability.keys():
                divisor = 1 + abs(student_ability[s] - B_AVG) / sqrt(B_VAR)
                Mij = 0
                if student_case_map[s][q] is not None:
                    Mij = student_case_map[s][q].score
                    count += 1
                temp += b / divisor * (100 - Mij)
            # 这里同样有两种处理方法，不知道取用哪一种
            temp /= len(student_ability.keys())
            # temp /= count
            case_difficulty[q] = temp
        print('迭代', i)
        print(case_difficulty)
        print(student_ability)


if __name__ == '__main__':
    score_evaluator_get_score_save(0)

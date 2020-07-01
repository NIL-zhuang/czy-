# 探索学生分组情况
import json

group_list = {}


def contain(list1, list2):
    # 判断list2是否真包含于list1
    for item in list2:
        if item not in list1:
            return False
    return True


if __name__ == '__main__':
    case_map = {}  # 题目集合
    question_list = []
    f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for student in data:
        cases = data[student]['cases']
        tmp = []
        for case in cases:
            tmp.append(case['case_id'])
        tmp = sorted(tmp)
        if len(tmp) >= 199:
            if len(question_list) == 0 or tmp[0] != question_list[-1][0]:
                question_list.append(tmp)
            # 把下面三行注释打开就知道为什么是五组题目了 不过有点奇怪有个做了206题的
            print('student', student, end=" ")
            print(len(tmp), end=" ")
            print(tmp)

    print("-----------------------------------")
    print("----------五组的题目分布如下-----------")
    for q in question_list:
        print(q)
    for index in range(len(question_list)):
        group_list[index] = []  # 有几组，就初始化几个key

    failure_user = {}
    print('正在分组中...')

    for student in data:
        found = False
        cases = data[student]['cases']
        tmp = []
        for case in cases:
            tmp.append(case['case_id'])
        for index in range(len(question_list)):
            if contain(question_list[index], tmp):
                # print('第', index, '组')
                group_list[index].append(student)
                found = True
                break
        if not found:
            print(student, '分组失败')
            failure_user[student] = tmp.copy()

    for group in group_list.keys():
        print('第', group, '组 人数共', len(group_list[group]))
        # print(group_list[group])

    for user in failure_user.keys():
        print(failure_user[user])
"""
@Author: Allen Lee       2018-03-06
"""
import pandas as pd
from compile.my_class import MyPath


def clean_labor_data(filename, in_service_only=True):
    NJ_department = ['南京新百', '南京大厂', '南京溧水', '南京泰山一部', '南京泰山二部', '南京六合']
    container = pd.DataFrame()

    def class_position(pos):
        if not isinstance(pos, str):
            return None
        elif '管理CF' in pos:
            return pos.replace('管理CF', '')
        elif '营销CF' in pos:
            return pos.replace('营销CF', '')

    for depart in NJ_department:
        print("loading department: %s" % depart)
        raw_dep = pd.read_excel(filename, depart)
        if in_service_only:
            raw_dep = raw_dep[raw_dep.loc[:, '是否在职'] == '在职']
        raw_dep['组织名称'] = depart
        raw_dep['城市'] = '南京市'
        raw_dep.loc[:, '对应职级'] = raw_dep.loc[:, '对应职级'].apply(class_position)
        raw_dep = raw_dep.reindex(columns=['储信贷注册手机号',
                                           '组织名称', '城市',
                                           '城市经理', '营业部经理',
                                           '团队经理', '姓名',
                                           '入职日期', '对应职级', '是否在职'])
        container = container.append(raw_dep, True)

    print("loading department: 世界广场")
    SH_dep = pd.read_excel(filename, '世界广场')
    if in_service_only:
        SH_dep = SH_dep[SH_dep.是否在职 == '在职']
    SH_dep['组织名称'] = '世界广场'
    SH_dep['城市'] = '上海市'
    SH_dep.loc[:, '对应职级'] = SH_dep.loc[:, '对应职级'].apply(class_position)
    SH_dep = SH_dep.reindex(columns=['绑定手机号', '组织名称',
                                     '城市', '城市经理',
                                     '营业部经理', '团队经理',
                                     '姓名', '入职日期',
                                     '对应职级', '是否在职'])
    container.rename(columns={'储信贷注册手机号': '绑定手机号'}, inplace=True)
    container = container.append(SH_dep, True)

    print("loading 兼职人员")
    JZ_dep = pd.read_excel(filename, '兼职人员')
    if in_service_only:
        JZ_dep = JZ_dep[pd.isnull(JZ_dep.备注)]
    else:
        JZ_dep['是否在职'] = '在职'
        JZ_dep.loc[:, '是否在职'] = JZ_dep.apply(lambda x: '在职' if pd.isnull(x.loc['备注']) else '离职', axis=1)
    JZ_dep['城市'] = '南京市'
    JZ_dep['对应职级'] = 'S1'
    JZ_dep = JZ_dep.reindex(columns=['电话', '营业部',
                                     '城市', '城市经理',
                                     '营业部经理', '团队经理',
                                     '姓名', '入职日期',
                                     '对应职级', '是否在职'])
    JZ_dep.rename(columns={"电话": "绑定手机号", '营业部': "组织名称"}, inplace=True)
    container = container.append(JZ_dep, True)
    container.rename(columns={"绑定手机号": "理财顾问手机号",
                              '姓名': '第1层',
                              '团队经理': '第2层',
                              '营业部经理': '第3层',
                              '城市经理': '第4层'}
                     , inplace=True)
    container.loc[:, '入职日期'] = container.loc[:, '入职日期'].astype('datetime64[ns]')
    container = container.sort_values(by='入职日期', ascending=False, na_position='last')
    container = container.sort_values(by='是否在职', ascending=True, na_position='last')
    container.drop_duplicates(['第1层'], keep='first', inplace=True)

    def mobile_no_fmt(x):
        if isinstance(x, str):
            try:
                x = int(x)
            except:
                pass
        return x

    container.loc[:, '理财顾问手机号'] = container.loc[:, '理财顾问手机号'].apply(mobile_no_fmt)
    return container


def main():
    path = MyPath().scriptpath
    input_file = input("Please set input file path:\n")
    output_path = input("Please set output file path, default path:\n%s\n" % path+r'\U_table.xlsx')
    keep_in_service = input("in-service only? [n]/y: ")
    if output_path == '':
        output_path = path+r'\U_table.xlsx'

    while keep_in_service not in ['y', 'n', '']:
        keep_in_service = input('[n]/y: ')

    if keep_in_service == 'y':
        keep_in_service = True
    elif keep_in_service == 'n' or '':
        keep_in_service = False

    cleaned_data = clean_labor_data(input_file, in_service_only=keep_in_service)
    cleaned_data.to_excel(output_path, 'Sheet2', index=False)
    print("New U_table extracted at %s" % output_path)


if __name__ == '__main__':
    main()

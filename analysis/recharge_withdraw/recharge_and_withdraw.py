"""
@Author: Allen Lee     2017-12-29
"""
from compile.my_class import *


def old_app_offline_recharge(start_date, end_date):
    sql = "select a.create_date,u.mobile_no,c.real_name,u1.mobile_no 邀请人,a.amount from t_sys_recharge a\
          left join t_bus_user u on a.user_name=u.user_name\
          left join t_bus_user_basic_info c on a.user_name=c.user_name\
          LEFT JOIN t_bus_user_invite_log l ON a.user_name=l.invited_user_name\
          LEFT JOIN t_bus_user u1 ON u1.user_name=l.user_name\
          where date(a.create_date)>=%s and date(a.create_date)<=%s\
          AND a.`status`='133002'\
          and u.role_id in ('ordinary','counselor')\
          and a.user_name not in ('AB4E6DAFAF504037BA58F76E728CD887',\
                                    '2EEC41510A864256A8BE93BF9F3D5276', \
                                    '987A08A3797147949528FEF5D7C0E90C')"
    cur = sql_connection()
    cur.execute(sql, (start_date, end_date))
    recharge = cur.fetchall()
    cur.close()
    return recharge


def old_app_offline_withdraw(start_date, end_date):
    sql = "select a.create_date,u.mobile_no,c.real_name,u1.mobile_no,a.expenditure from t_bus_financial_details a\
          left join t_bus_user u on a.user_name=u.user_name\
          left join t_bus_user_basic_info c on a.user_name=c.user_name\
          LEFT JOIN t_bus_user_invite_log l ON a.user_name=l.invited_user_name\
          LEFT JOIN t_bus_user u1 ON u1.user_name=l.user_name\
          where date(a.create_date)>=%s and date(a.create_date)<=%s\
          and details_type='104002' \
          and u.role_id in ('ordinary','counselor')\
          and a.user_name not in ('AB4E6DAFAF504037BA58F76E728CD887',\
                                    '2EEC41510A864256A8BE93BF9F3D5276', \
                                    '987A08A3797147949528FEF5D7C0E90C')"
    cur = sql_connection()
    cur.execute(sql, (start_date, end_date))
    withdraw = cur.fetchall()
    cur.close()
    return withdraw


def old_app_online_recharge(start_date, end_date):
    sql = "select a.create_date,u.mobile_no,c.real_name,a.amount from t_sys_recharge a\
          left join t_bus_user u on a.user_name=u.user_name\
          left join t_bus_user_basic_info c on a.user_name=c.user_name\
          LEFT JOIN t_bus_user_invite_log l ON a.user_name=l.invited_user_name\
          LEFT JOIN t_bus_user u1 ON u1.user_name=l.user_name\
          where date(a.create_date)>=%s and date(a.create_date)<=%s\
          AND a.`status`='133002'\
          and u.role_id not in ('counselor','special','ordinary')"
    cur = sql_connection()
    cur.execute(sql, (start_date, end_date))
    recharge = cur.fetchall()
    cur.close()
    return recharge


def old_app_online_withdraw(start_date, end_date):
    sql = "select a.create_date,c.real_name,u.mobile_no,a.expenditure from t_bus_financial_details a\
          left join t_bus_user u on a.user_name=u.user_name\
          left join t_bus_user_basic_info c on a.user_name=c.user_name\
          LEFT JOIN t_bus_user_invite_log l ON a.user_name=l.invited_user_name\
          LEFT JOIN t_bus_user u1 ON u1.user_name=l.user_name\
          where date(a.create_date)>=%s and date(a.create_date)<=%s\
          and details_type='104002'\
          and u.role_id not in ('counselor','special','ordinary')\
          AND u.sys_flag!=2"
    cur = sql_connection()
    cur.execute(sql, (start_date, end_date))
    withdraw = cur.fetchall()
    cur.close()
    return withdraw


def cg_recharge(start_date, end_date):
    print('loading cg recharge...')
    sql = "SELECT * FROM(\
          SELECT d.transaction_time,u.mobile_no,b.real_name,d.amount FROM cg_recharge_detail d\
          left join t_bus_user u on d.user_name=u.user_name\
          left join t_bus_user_basic_info b on d.user_name=b.user_name\
          WHERE disabled = 0\
          AND bus_sataus = 1\
          AND recharge_type=0\
          AND date(d.transaction_time)>=%s and date(d.transaction_time)<=%s\
          UNION\
          SELECT d.transaction_time,u.mobile_no,b.real_name,d.amount\
          FROM cg_recharge_detail d\
          left join t_bus_user u on d.user_name=u.user_name\
          left join t_bus_user_basic_info b on d.user_name=b.user_name\
          WHERE d.disabled = 0\
          AND d.recharge_type = 1\
          AND d.bus_sataus = 1\
          AND date(d.transaction_time)>=%s and date(d.transaction_time)<=%s\
          UNION\
          SELECT modify_time,u.mobile_no,b.real_name,operation_amount FROM cg_replace_recharge d\
          left join t_bus_user u on d.user_name=u.user_name\
          left join t_bus_user_basic_info b on d.user_name=b.user_name\
          WHERE disabled = 0\
          AND apply_status=2\
          AND date(d.modify_time)>=%s and date(d.modify_time)<=%s)a\
          ORDER BY a.transaction_time ASC"
    cur = sql_connection()
    cur.execute(sql, (start_date, end_date, start_date, end_date, start_date, end_date))
    recharge = cur.fetchall()
    cur.close()
    return recharge


def cg_withdraw(start_date, end_date):
    sql = "SELECT a.transaction_time,u.mobile_no,b.real_name,a.arrival_amount\
          FROM cg_withdraw_apply a\
          left join t_bus_user u on a.user_name=u.user_name\
          left join t_bus_user_basic_info b on a.user_name=b.user_name\
          WHERE disabled = 0\
          AND bus_sataus = 1\
          AND date(a.transaction_time)>='%s' \
          AND date(a.transaction_time)<='%s'\
          ORDER BY a.transaction_time ASC" % (start_date, end_date)
    cur = sql_connection()
    cur.execute(sql)
    withdraw = cur.fetchall()
    cur.close()
    return withdraw


if __name__ == '__main__':
    mytool = MyPath()
    mytime = MyDate()
    to_csv = mytool.to_csv
    today = mytime.curdate
    last_saved = mytime.last_saved
    yesterday = mytime.yesterday
    day_after_last_saved = mytime.day_after_last_saved

    print("@Author: Allen Lee\t2018-01-10\n请勿关闭此窗口，稍等约1分钟...")

    to_csv('cg_recharge', cg_recharge(last_saved+' 16:00:00', today+' 15:59:59'),
           ('时间', '手机号', '姓名', '充值金额'))
    print("cg_recharge complete")
    to_csv('cg_withdraw', cg_withdraw(day_after_last_saved, today),
           ('时间', '姓名', '手机号', '提现金额'))
    print("cg_withdraw complete")
    to_csv("old_app_offline_recharge", old_app_offline_recharge(last_saved, yesterday),
           ('时间', '手机号', '姓名', '邀请人', '充值金额'))
    print("old_app_offline_recharge complete")
    to_csv('old_app_offline_withdraw', old_app_offline_withdraw(day_after_last_saved, today),
           ('时间', '手机号', '姓名', '邀请人', '提现金额'))
    print("old_app_offline_withdraw complete")
    to_csv('old_app_online_recharge', old_app_online_recharge(last_saved, yesterday),
           ('时间', '手机号', '姓名', '充值金额'))
    print("old_app_online_recharge complete")
    to_csv('old_app_online_withdraw', old_app_online_withdraw(day_after_last_saved, today),
           ('时间', '姓名', '手机号', '提现金额'))
    print("old_app_online_withdraw complete")

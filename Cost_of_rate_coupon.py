print("loading...\n")
from pandas import DataFrame
from compile.my_class import sql_connection
import sys


def ticket_type():
    sql = "select id,up_apr_max_datetime,ticket_amount\
    from cg_card_ticket where ticket_type_code in %s and status=5 and date(create_time) between '%s' and '%s';" \
          % (ticket_type_code, start_date, end_date)
    cur = sql_connection()
    cur.execute(sql)
    ticket = cur.fetchall()
    if ticket != ():
        ticket = DataFrame(list(ticket), columns=("id", "interest_period", "amount"))
        print("Fetching ticket information Done.")
        cur.close()
        return ticket
    else:
        print("Please check your ticket_type_code or date period.")
        cur.close()
        sys.exit()


def ticket_detail():
    sql = "select amount,interest_amount,extend1\
        from cg_card_ticket_income_detail where status=2;"
    cur = sql_connection()
    cur.execute(sql)
    detail = cur.fetchall()
    detail = DataFrame(list(detail), columns=("principal", "interest_amount", "extend1"))
    cur.close()
    return detail


#加息券配对：
def interest_amount():
    ticket = ticket_type()
    detail = ticket_detail()
    payment_in_set = []
    for i, drow in enumerate(detail.values):
        for j, trow in enumerate(ticket.values):
            if str(trow[0]) in drow[2].split(','):
                payment_in_set.append(drow)

        percent = 100*(i+1)/detail.shape[0]
        if i % int(detail.shape[0]/10) == 0:
            print("Matching in process:%.1f%%" % percent)

    payment_in_set = DataFrame(payment_in_set, columns=("principal", "interest_amount", "extend1"))
    return payment_in_set


def main():
    payment_in_set = interest_amount()
    principal = payment_in_set.principal

    ticket = ticket_type()
    simple_interest = ticket.amount[0] / 36500
    cost = principal * simple_interest
    return sum(cost)


if __name__ == '__main__':
    ticket_type_code = input("Set ticket_type_code:\n").split(',')
    start_date = input("Set start date:\n")
    end_date = input("Set end date:\n")
    if len(ticket_type_code) > 1:
        ticket_type_code = str(tuple(ticket_type_code))
    else:
        ticket_type_code = '("%s")' % ticket_type_code[0]

    print("The Cost of Rate Coupon is %.2f" % main())
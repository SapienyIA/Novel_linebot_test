import time
import schedule
import threading
import novel_linebot as lb

def check():
    print("-----"*5,"檢查中","-----"*5)
    lb.sc.check_update2()

def sch():
    while 1:
        schedule.run_pending()
        time.sleep(1)

schedule.every().hours.do(check)

if __name__ == "__main__":
    thread = threading.Thread(target=sch)
    thread2 = threading.Thread(target=lb.run_server)
    thread.start()
    thread2.start()
    time.sleep(3)

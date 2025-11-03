import socket
from database import get_connection

def get_ip():
    try:
        hostname=socket.gethostname()
        ip_address=socket.gethostbyname(hostname)
        return ip_address
    except:
        return "unknown"
    
def checkip(ip_address):
    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT ip_address FROM blocked_ips WHERE ip_address=?", (ip_address,))
    result=c.fetchone()
    return result is not None

def blockip(ip_address):
    conn=get_connection()
    c=conn.cursor()
    c.execute(
        """
    SELECT COUNT(DISTINCT username)
    from login_history
    where ip_address=? and success=0

""",(ip_address,)
    )
    result=c.fetchone()
    count=result[0]

    if(count>3):
        c.execute("INSERT INTO blocked_ips (ip_address) VALUES (?)", (ip_address,))
        print("IP address blocked")

    conn.commit()
    conn.close()
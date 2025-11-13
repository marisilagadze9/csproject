# User Authentication System

This is a small web application where people can register, log in, and use a secure authentication system. It not only keeps user accounts safe but also tries to block any suspicious activity or repeated failed login attempts from the same IP.

---

## What the app does
- Lets users register with secure passwords
- Allows users to log in with password verification
- Blocks accounts after 5 failed login attempts
- Blocks IPs if there are repeated failed login attempts from the same IP
- Admin panel to view the login history

---

## Database structure
**users** – stores users and their passwords  
**login_history** – records every login attempt, the IP used, and whether it was successful  
**blocked_ips** – keeps track of blocked IP addresses  

---

## Security features
- Passwords are stored in a hashed form (SHA-256 + salt)
- Multiple failed login attempts will block the account
- IP blocking protects against repeated attacks
- All login attempts are recorded with timestamps and IP addresses  

---



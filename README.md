# Distributed-temperature-control-system
A course work that simulate the temperature control in hotel, including two part: MainController( for administrator), AirCondition(for customer)

## Functions for it:
**Main Controller:**
1. Administrator Login
2. Set Refresh frequency
3. Check each room's status:
   including: Room ID, Room temperature, current Fee, current Energy, current wind Speed
4. Check out for the customer.
5. Generate report (daily/weekly/yearly)

**AirCondition:**
1. Customer Login
2. Modify the temperature and wind speed
3. Check the status:
   including: mode - summer/winter,  current energy used, current Fee, room temperature, target temperature, current wind speed
4. Power off the machine

### Requirement
Python 3.5
pip install pyecharts==0.5.11
pip install pyechars-snapshot

### How to run it?
Run main.py in MainController Folder to start a administrator's application.
Run main.py in AirCondition Folder to start a customer application.
The two application can run in different computer, but remeber to modify the ip address in AirCondition/Connection, it should be the ip address of corresponding MainController.

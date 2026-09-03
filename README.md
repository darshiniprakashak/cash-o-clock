<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# Cash-O-Clock 🎯


## Basic Details
### Team Name: Code Red


### Team Members
- Team Lead: Darshini Prakash A K - LBSITW
- Member 2: Ahna Shajahan - LBSITW
  

### Project Description
Cash-O-Clock is a gamified alarm clock website that turns morning laziness into a real-time financial consequence. By leveraging automated UPI debits, hitting snooze instantly transfers a monetary penalty to a rival or designated recipient, ensuring you either wake up on time or pay the price.

### The Problem (that doesn't exist)
Every morning, millions of ambitious humans suffer from Chronological Denial Syndrome—a dangerous delusion where your brain genuinely believes that sleeping for 300 extra seconds will fix your life, rather than make you late for work. Traditional alarms offer infinite mercy with zero consequences, allowing your half-asleep self to completely destroy the goals of your night-time self. Loud beeps and math puzzles fail because sleep-deprived brains adapt quickly, leaving us with a system where bed warmth always wins over self-discipline.

### The Solution (that nobody asked for)
Rather than fixing your sleep habits, **Cash-O-Clock** weaponizes capitalist dread by turning your snooze button into a high-risk financial terminal. If willpower won't drag you out of bed, watching ₹50 instantly fly out of your UPI account directly to your arch-rival definitely will—making laziness literally too expensive to afford.

## Technical Details
### Technologies/Components Used
For Software:
- Languages used : Python
- Frameworks used: Streamlit
- Libraries used: streamlit, requests, qrcode, datetime, time, io.BytesIO
- Tools used: Visual Studio Code, Git, Uvicorn, FastAPI (Backend)

### Implementation
For Software:
 # **Installation**
   **Clone the repository**
  git clone https://github.com/your-username/cash-o-clock.git
  cd cash-o-clock

  # **Install required dependencies**
  pip install streamlit requests qrcode pillow

 # **Run**
   https://cash-o-clock-bkscgftlgayjiaivmvdgmx.streamlit.app/

### Project Documentation
For Software:

# Screenshots (Add at least 3)
<img width="1642" height="980" alt="Welcome Screen" src="https://github.com/user-attachments/assets/4cd347a6-cb22-4031-bd5b-ec8da91ee49d" />

This screenshot shows the landing page (welcome screen) of the Cash-O-Clock web application. It acts as the initial entry point for users before they configure their alarm settings or launch the interactive setup dashboard.

<img width="1172" height="988" alt="Dashboard" src="https://github.com/user-attachments/assets/a9097099-3835-4a71-948c-633103dbdfda" />

This screenshot shows the **Main Dashboard & Alarm Setup Page** of the **Cash-O-Clock** application, where users configure their alarm parameters and monitor their snooze statistics.

* Stats Dashboard: Features two summary cards displaying real-time metrics—**Total Penalty Paid** (currently ₹5) and **No. of Snoozes** (currently 1).
* Victory Alert Banner: Displays a success message (*"VICTORY! Alarm turned off on time! Zero funds debited."*) confirming the user previously disabled the alarm without incurring a snooze penalty.
* Penalty & Payment Configuration: Includes a slider to select the **Snooze Penalty Amount** (set to ₹5) and a text field to enter the **Destination UPI ID** where penalty funds will be sent.
* Alarm Controls: Contains a time picker field to set the target alarm time (set to 06:30) alongside two trigger options—**Activate Alarm** (schedules the alarm for the selected time) and **DEMO MODE: Ring Alarm Instantly** (triggers the ringing screen immediately for testing).

<img width="1250" height="951" alt="Alarm Screen" src="https://github.com/user-attachments/assets/d2d9c090-1957-4258-9fd6-df72cc3101ee" />
This screenshot shows the **Active Alarm Screen (Ringing State)** of the **Cash-O-Clock** application, which triggers when the scheduled alarm time is reached or launched via Demo Mode.

* Alert Header: Displays an animated ringing alarm clock icon accompanied by high-urgency warnings: *"🚨 WAKE UP OR PAY UP! 🚨"* and *"Your sleep is getting expensive! 💸"*.
* Penalty Display Card: Highlights the real-time financial consequence for snoozing—showing **₹5** as the mandatory cost to go back to sleep.
* SNOOZE (PAY ₹5): Primary coral-red button that debits the penalty fee, updates the total penalty counter, and generates a UPI QR code payment link.
* ALARM OFF (I'M AWAKE): Secondary dark-card button with a yellow border that safely disarms the alarm without deducting any funds.

<img width="840" height="1027" alt="image" src="https://github.com/user-attachments/assets/78a13186-ad48-4b3e-9696-74088c5555db" />

This screenshot shows the **Payment Receipt & UPI Authorization Screen** of the **Cash-O-Clock** application after the user presses the snooze button.

* **Updated Dashboard Stats:** The **Total Penalty Paid** counter has increased to **₹5** and the **No. of Snoozes** counter shows **1**, reflecting the user's decision to snooze.
* **Transaction Details Card:** Displays a red notification alert confirming that a payment has been triggered, detailing the **Amount (₹5)**, **Recipient (`yourname@okaxis`)**, and a generated **Reference Code (`REF_2E80288E`)**.
* **Dynamic UPI QR Code:** Renders an auto-generated QR code for instant scanning with UPI payment apps like Google Pay, PhonePe, or Paytm.
* **Direct Deep Link:** Includes a clickable link (*"👉 Click here to pay directly via UPI App"*) allowing mobile users to open their preferred UPI app directly.
* **Reset Setup Panel:** Below the receipt, the alarm setup configuration re-renders, enabling the user to adjust settings or reactivate the alarm for another cycle.

# Diagrams
<img width="647" height="1012" alt="DIAGRAM-WORKFLOW" src="https://github.com/user-attachments/assets/84b91105-75a4-4ee0-8a78-3b344d6678fd" />

System Workflow Architecture
This diagram maps out the end-to-end user journey and data processing logic within the Cash-O-Clock application:

Entry & Setup: The user enters through the landing page to access the main dashboard, configuring their preferred snooze penalty amount, target receiver UPI ID, and alarm time.

Alarm Trigger: Once activated (or triggered instantly via Demo Mode), the app transitions into an active ringing state with continuous audio feedback and financial warning prompts.

Disarm Path: Selecting "ALARM OFF" silences the alarm immediately, updates the dashboard with a success victory message, and incurs zero financial penalty.

Penalty Path (Snooze): Selecting "SNOOZE" sends a POST request to the backend /api/snooze endpoint to generate a unique transaction reference and dynamic UPI deep-link. The frontend then updates session metrics (incrementing total penalty paid and snooze count) and renders an auto-generated QR code alongside a direct payment link for immediate UPI authorization (via GPay, PhonePe, or Paytm).

### Project Demo
# Video
https://photos.app.goo.gl/axZHRFRp5xwkALyU6
Terminal Execution (0:00 - 0:04): The video starts in VS Code, showing the Streamlit application launching in the terminal via streamlit run app.py.

Landing Screen (0:05 - 0:08): The browser opens to the dark-themed Cash-O-Clock landing screen. Clicking the "LAUNCH CASH-O-CLOCK" button transitions into the setup dashboard.

Configuring Snooze Penalty (0:09 - 0:17): On the setup dashboard, the initial stats show ₹0 paid and 0 snoozes. The user adjusts the Snooze Penalty Amount slider from the default ₹5 up to ₹50.

Alarm Trigger (0:18 - 0:28): The user clicks "DEMO MODE: Ring Alarm Instantly" to trigger the alarm screen. The UI switches to the ringing state with a pulsing alarm clock and the warning banner "WAKE UP OR PAY UP!", showing the newly configured ₹50 penalty cost.

Snooze & Payment Generation (0:29 - 0:38): Clicking "SNOOZE (PAY ₹50)" immediately updates the session stats to ₹50 Total Penalty Paid and 1 Snooze. Below the stats, the app displays a transaction alert block with reference code REF_7FE2959E and generates a dynamic UPI QR code alongside a deep link to authorize the ₹50 payment.

## Team Contributions
- Ahna Shajahan: Designed the Streamlit frontend UI/UX, implemented custom CSS themes, landing page navigation, and state management for snooze stats and penalty counters.

Darshini Prakash A K: Implemented the backend integration, dynamic UPI payment link generation, QR code rendering logic, and audio/alarm trigger mechanisms.
---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)




# CAN Bus Monitoring Tool for the EESC-USP Tupã Automotive Prototype

Data acquisition plays a vital role in engineering, enabling early detection of design flaws and providing insights into system behavior under challenging conditions. In the automotive sector, this process is essential — not only for validating concepts but also for identifying failures before they lead to incidents.
This project focuses on developing a low-cost, architecture-independent data logging device designed to support the validation of the EESC-USP Tupã team’s prototype. The need for such a tool arose from the team's yearly design updates, which often disrupt telemetry systems.
To address this challenge, we built a system that monitors the prototype’s CAN bus and transmits data via the LoRa protocol to a receiver. The receiver then processes and displays the information on a computer in a clear and intuitive format. The solution was designed to meet key team requirements, such as antenna range exceeding the track length and seamless visualization of parameters—without interfering with the prototype’s architecture or internal communications.
This tool has the potential to streamline manufacturing and validation processes for future projects, enhancing both testing efficiency and performance analysis

## Objectives
The goal of this project is to develop a low-cost data logging device that operates independently of the vehicle’s architecture, aimed at validating the EESC-USP Tupã team’s automotive prototype. The need for such a device became evident due to the team's yearly design changes, which often compromise telemetry systems. While some national and international teams already use data logging tools, these solutions tend to be expensive.

The main responsibility of the proposed device is to record data transmitted over the vehicle’s CAN network and apply a __timestamp__ to each entry. This data will then be sent to a database for future analysis. Alongside the logging device, a __dashboard__ will also be developed to display the collected information in a clear and accessible format.

---

# Example Execution Using a Jakarta Bus Database
To demonstrate the system in action, I used a public transportation dataset from Jakarta, focusing specifically on bus routes and schedules. 

<img width="961" height="942" alt="dashboard_2" src="https://github.com/user-attachments/assets/1c38b56e-a838-42be-b57e-6a5314c15b97" />


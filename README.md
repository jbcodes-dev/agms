# Final Year Project

Repository for my Final Year Project of my Software Engineering Degree.

## Microgreen Growth Management within a Terrarium

This project creates and utilises an algorithm for optimising the growth of Microgreens within a Terrarium environment by monitoring sensor values for Temperature, Humidity, and Soil Moisture Level to control relays to engage the Airflow, Irrigation, and Lighting systems. 

The data from each sensor and relay is uploaded into an SQLite3 database that is then accessed by a webpage to provide graphics of historical data using Chart.js. This webpage can be accessed by VPN onto the private network the Raspberry Pi is connected to. Apache provides the webserver configurations for the device. 

Enabling port-forwarding on the router would allow for easier access to the webpage from any device. From a network security standpoint, this would pose a significant security threat to the local network if proper security measures were not put in place. Due to the scope of the project in addition to the time constraints, it was deemed unnecessary to go to these lengths, as the project does not require public access to the system, only the user who's terrarium it is.

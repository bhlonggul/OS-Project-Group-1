# OS-Project-Group-1
CPSC 351 Term Group Project

**Group 1:** Brian Hlonggul, Nicholas Legaspi, Ngoc Le, Colin Mercado, Franklin Cruz

## Group Members & Roles
| Member | Role |
| :--- | :--- |
| Ngoc Le | Team Lead / Project Director |
| Brian Hlonggul | Coding and Algorithm Implementations |
| Colin Mercado | Coding and Algorithm Implementations |
| Nicholas Legaspi | Output, Visualization, and Presentation |
| Frank Cruz | Presentation Slides |

## How to Run the Code
This project is written in standard Python and does not require any external libraries.
1. Clone this GitHub repository or download the files to your local machine.
2. Open the project folder in VS Code.
3. Open the `Kitchen_Scheduler.py` file.
4. Click the Run button in the top right corner of the editor.

## Story
A restaurant operates like a scheduling environment because multiple orders arrive. They must be handled with limited resources like chefs, stoves, or prep stations. For example, a very popular restaurant during rush hour, where the kitchen must decide which orders need to be prepared first. In this scenario, customer orders could represent the arrival time based on when the order was placed. A burst time can be determined by how long it takes to prepare the dishes. Lastly, priority levels can depend on urgency, such as delivery/take-out deadlines, VIP customers, or quick meals like appetizers. Each order represents a process waiting to be handled by the chefs, who we could define as the CPU. Since kitchen space and staff are limited resources, the order in which meals are prepared will significantly affect customer satisfaction. If scheduling is handled poorly, customers may wait too long, causing delays, complaints, and even wasted food. Effective scheduling ensures fairness, improves responsiveness for meals, and prevents starvation when certain orders are delayed.

## Chosen Algorithms
To test how our kitchen runs, we implemented three different scheduling algorithms:
* **FIFO (First-In, First-Out):** This mimics a standard ticket rail where orders are cooked strictly in the exact order they were placed. It guarantees absolute fairness because no one gets to cut the line.
* **SJF (Shortest Job First - Non-Preemptive):** This prioritizes efficiency by cooking the dishes with the shortest prep times first. In a real kitchen, this is like rushing out all the quick appetizers or salads to keep the dining room happy while the big entrees wait.
* **Round Robin (Quantum = 3):** This represents a chef rotating their attention among all active tickets so every customer sees some progress. We set our Time Quantum to 3 minutes, meaning the chef might sear a steak for 3 minutes, then immediately pivot to tossing a salad for 3 minutes before coming back.

**Our Input Data:**
| Order ID | Dish Context | Arrival Time | Burst Time (Cook Time) |
| :--- | :--- | :--- | :--- |
| 01 | Steak (well-done) | 0 min | 10 min |
| 02 | Caesar Salad | 1 min | 3 min |
| 03 | Pasta | 2 min | 7 min |
| 04 | Burger | 3 min | 5 min |
| 05 | Fries (appetizer) | 4 min | 2 min |

**Output Results Comparison:**
| Algorithm | Average Turnaround Time | Average Waiting Time |
| :--- | :--- | :--- |
| **FIFO** | 17.00 mins | 11.60 mins |
| **SJF** | 14.80 mins | 9.40 mins |
| **Round Robin (Q=3)** | 17.60 mins | 12.20 mins |

## Key Analysis
First, we observed the "Convoy Effect" with **FIFO**. We had the 10-minute, well-done steak arrive first (at minute 0), so all other tickets had to wait. The 2-minute fries arrived at minute 4, but could not start cooking until minute 25. This was generally fair, but it led to bad average waiting times.

**SJF** was the clear winner purely based on the results, giving us the lowest average turnaround time at 14.80 mins and the lowest average waiting time at 9.40 mins. By letting the fast items like the fries and salad jump ahead of the burger and pasta once the chef finished the steak, the kitchen cleared tickets much faster. However, the trade-off is huge: if waiters keep ringing in quick appetizers, a large order like the Pasta will suffer and never get cooked.

Finally with our last algorithm, **Round Robin** actually gave us the worst averages with a wait time of 12.20 mins. The chef physically bouncing between stations every 3 minutes causes a lot of context-switching overhead. However, in a real restaurant, this might actually be the most responsive method. Instead of the guy who ordered a salad waiting 25 minutes for a steak to finish, everyone gets their food gradually. It shows that the algorithm with the best "speed" isn't always the one that creates the best user experience.

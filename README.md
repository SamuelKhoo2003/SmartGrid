# Smart Grid - Energy Trading Simulation

<details>
<summary><strong>About</strong></summary>

In the rapidly advancing field of energy management, our Smart Grid project explores the integration of renewable energy with intelligent grid systems. The project focuses on optimizing the trading and storage of energy between an off-grid solar system and an external energy grid. By leveraging machine learning, optimization algorithms, and modern web technologies, this project aims to create a highly efficient and sustainable energy management system.

</details>

<details>
<summary><strong>Key Features</strong></summary>

- **Internal Solar Array:** The smart grid is powered by an internal solar array, which serves as the primary renewable energy source. This array plays a crucial role in reducing reliance on external energy sources.

- **Machine Learning Predictive Models:** Custom neural networks, developed using genetic algorithms, are employed to predict energy production, consumption patterns, and market prices. These models help in making informed decisions about energy trading.

- **Optimization Algorithms:** The project incorporates Mixed Integer Linear Programming (MILP) and MPPT (Maximum Power Point Tracking) techniques to optimize decisions on energy storage, usage, buying, and selling. The system recalibrates in real-time to maximize economic efficiency.

- **Microcontroller Management:** The smart grid system utilizes six microcontrollers—three dedicated to managing load usage and three for controlling energy flow through a Switched-Mode Power Supply (SMPS) module. This setup allows for precise control of energy distribution within the grid.

- **Web Application:** A React.js web application provides a user-friendly interface for monitoring and managing the smart grid. The dashboard displays real-time data on energy trading decisions, storage levels, and financial performance.

- **Cloud Integration:** The project features a robust AWS infrastructure with DynamoDB for data storage and API endpoints that connect solar grid hardware via Raspberry Pis. This setup ensures seamless integration and efficient data exchange between the hardware and the cloud.

</details>

<details>
<summary><strong>Simulation Overview</strong></summary>

The smart grid model simulates a single day, with each simulated minute represented by a 5-minute interval. This granularity allows for detailed analysis and optimization of energy flows throughout the day. The system continuously updates its predictions and optimizations to reflect real-time conditions.

</details>

<details>
<summary><strong>Project Report</strong></summary>

The accompanying project report provides a comprehensive overview of the system's design, implementation, and performance. It details the development process, the challenges faced, and the solutions devised to create an efficient and scalable smart grid system. The report also includes an analysis of the system's performance, demonstrating the effectiveness of the machine learning models and optimization algorithms in managing energy trading and storage.

</details>

<details>
<summary><strong>Running the Code</strong></summary>

To run the project, install all required dependencies using:

```bash
pip install -r requirements.txt
```

This will set up the environment needed to execute the smart grid simulation and web application.

</details>

<details>
<summary><strong>Top-Level Design</strong></summary>

The top-level design of the smart grid system is visualized in the following diagram:

![Top-Level Design](https://github.com/SamuelKhoo2003/SmartGrid/blob/main/images/TopLevel.drawio.png)

This diagram illustrates the key components of the system, including the solar array, microcontrollers, SMPS module, and the cloud integration.

</details>

<details>
<summary><strong>Buy-Sell Algorithm</strong></summary>

### Machine Learning Predictions

A custom genetic algorithm was developed to train a population of neural networks for predicting buy prices, sell prices, and energy demand. The algorithm selects the best-performing neural networks based on a fitness score derived from the reciprocal of the mean squared error. Over multiple epochs, the algorithm evolves the neural networks through processes such as crossover and mutation, optimizing them for accurate predictions.

### Optimization

The optimization process is driven by a Coin and Branch or Cut (CBC) solver, a Mixed Integer Linear Programming (MILP) library. The solver maximizes profit by making optimal decisions on energy trading over a prediction window of 60 ticks. The system recalibrates at each tick to ensure that decisions are based on the most recent data.

</details>

<details>
<summary><strong>Web Application</strong></summary>

### Dashboard

The web application's dashboard provides real-time insights into the smart grid's operations. It displays key metrics such as whether the system is buying or selling energy, historical storage data, and a comparison of the MILP algorithm's performance against a naive solution.

### Consumption and Finance Pages

The web application also features detailed pages for monitoring energy consumption and financial performance, providing users with a comprehensive view of the smart grid's efficiency and profitability.

### Demo

A live demo of the web application can be accessed [here](#) (Insert the actual URL).

</details>


# Week 7 Transcript

## Status Update and Deployment

### 00:00:20

**Customer:** Is it not deployed on the VM?

**Team:** No, not yet. We just pushed the latest version to GitHub. I will deploy the fully completed version this evening.

**Customer:** You mentioned last week that the VM version was outdated. Is it still the case?

**Team:** Yes, that was about a week ago. We will deploy the actual final version on the VM after the meeting.

---

### 00:02:00

**Team:** So, what's new? The user interface has changed significantly. Regarding patterns, the database integration is now complete. Currently, all patterns are saved in the database. Before the project initializes for the user, all coins are analyzed by the ML model. When a user logs in, they can click "Analyze," and the entire chart (all 50,000 candles) is processed instantly because it retrieves the pre-calculated ML results from the database.

---

## ML Analysis Flow & Concurrency

### 00:03:00

**Customer:** How often is new data added to the database? Or rather, how often do you check if a new pattern has appeared?

**Team:** This happens when the user clicks "Analyze." Any candles that have not been analyzed yet are processed at that moment.

### 00:03:40

**Customer:** Do you have any validation to handle concurrent requests? For example, if two users click "Analyze Patterns" simultaneously from different computers, how many times will the backend process the request? What goes into the database? Is there any check in place?

**Team:** The analysis runs before project initialization. It records everything in the database, then scans the latest candles to ensure the entire chart is covered. When you click "Analyze," it first retrieves data from the database, then analyzes the most recent candles that were just loaded.

### 00:05:10

**Customer:** How does it determine which candles are the "latest"? How does it track which candles have been analyzed?

**Team:** There is a variable storing the timestamp of the last analyzed candle. It is stored in the database.

### 00:06:15

**Customer:** I want to understand the project's performance. If a thousand people click "Analyze Patterns" simultaneously, what happens?

**Team:** It will load instantly for everyone. If one user clicks, their latest candles are analyzed and the database is updated. The new 50 candles will be analyzed — at most 150 candles. The ML model analyzes them in approximately 0.01 seconds.

### 00:08:05

**Customer:** What is the table structure in the database? How are patterns stored?

**Team:** Let us inspect the database. (Attempts to enter the Docker container terminal)

---

## Database Schema Inspection

### 00:08:50

**Team:** We can look at the database, but we are having some difficulty entering the container terminal on this machine.

**Customer:** How do you usually check what is in the database? Do you verify it from the frontend?

**Team:** We mostly verified functionality from the frontend. Let me explain the logic instead.

### 00:10:20

**Customer:** This point is crucial for understanding performance. You said that before initialization, all coins are analyzed. But where do the existing candles come from if the database is created fresh in the container?

**Team:** When you create the project for the very first time, it fetches historical data via the Bybit API. The backend algorithm populates the database. First, it fetches the candles, and then it analyzes them.

### 00:11:45

**Customer:** How long does it take to retrieve candles from the Bybit API?

**Team:** It takes about 2–3 minutes for all 10 coins. But that is only for the initial initialization. The next time you run Docker locally, it will load instantly because everything is already in the database. This prevents hitting API rate limits. Plus, the ML model takes about a minute to process everything.

---

## New Features Demonstration

### 00:14:00

**Team:** I added a sidebar that allows adding other coins — an unlimited number — plus a search function for convenience. This makes the project scalable.

Next, the indicators have been changed. They now work correctly, similar to TradingView. You can move them around. Previously, they overlapped; now they work fine.

We also added metrics: price changes over 5 minutes, 1 hour, and 4 hours, as well as market cap and supply. This data is fetched from the CoinGecko API — the same one we use for icons. Some of these metrics are calculated based on candle data.

### 00:15:30

**Team:** Regarding the filter: it is located next to the patterns. By default, everything is enabled. You can toggle patterns on and off. Everything works.

---

## Machine Learning Update

### 00:16:15

**Team:** Danila, can you explain the ML updates?

**ML Team:** There is already a pull request on the new branch. I added analysis for Double Top (DT) and Double Bottom (DB) patterns and slightly modified the API so it can be integrated on the backend. The old pipeline for analyzing DT/DB patterns alongside Head and Shoulders (HS) and Inverse Head and Shoulders (InHS) will continue to work. The API remains backward compatible.

**Customer:** How will these patterns be displayed on the frontend?

**Team:** On the frontend, it will be identical to HS and InHS.

**Customer:** What about accuracy?

**ML Team:** Recall is around 80%. Precision for DT/DB is about 17–18%.

---

## Container & Deployment Discussion

### 00:18:05

**Customer:** If we spin up all containers, will everything work 100%?

**Team:** But you need to install the necessary libraries first.

**Customer:** We discussed adding requirements to a text file and including them in the project.

**Team:** Not all dependencies are in the container. For example, NPM was not installed inside the container.

**Customer:** Is your frontend running as a container or not?

**Team:** Yes. Ideally, the container should contain both backend and frontend.

### 00:19:55

**Customer:** Please show the backend Dockerfile.

**Team:** (Opens Dockerfile) Yes, the frontend is included. Everything works perfectly.

**Customer:** Did you successfully launch it via the Dockerfile?

**Team:** Yes, normally. Everything works.

**Speaker 5:** If it works, then it is good. Generally, this is not standard practice, but since this is a small course and an MVP, it is acceptable overall.

---

## Defense & Grading

### 00:22:05

**Customer:** So, is your defense on Monday? Or Wednesday?

**Team:** The 21st. Tuesday.

**Customer:** Are you ready for the defense?

**Team:** Well, we will make a presentation, so yes, we are ready.

**Customer:** And you are defending before the TAs, correct?

**Team:** Yes, there will be three TAs.

**Customer:** What grades did you get on the assignments?

**Team:** Mostly 0.8 (80%). There was one 100%. Grades are reduced for documentation issues. They check strictly.

**Customer:** Understood. So, we expect the final version this evening, correct?

**Team:** Yes, yes, this version.

**Customer:** And we will be able to just run and check it.

**Team:** Yes, yes, yes.

---

## Outstanding PBIs

### 00:24:20

**Team:** Have we satisfied all the requests regarding these PBIs?

**Customer:** Well, you asked a lot about anomalies, but unfortunately, there are no anomalies.

**Team:** Yes, we simply ran out of time. Danila just finished with DT and DB yesterday. Anomaly detection turned out to be more complex than we thought.

**ML Team:** If there were any data or research available online on this topic, it would have been feasible. But everything written about ML in this area consists of personal ideas and tests. I had many ideas that I did not even have time to test. Some were skipped due to time constraints, others because the dataset was too small.

---

## Team Reflections

### 00:25:45

**Customer:** But still, well done for researching and implementing despite the lack of information online. I hope it was interesting. Overall, how did you find the project? Did you enjoy working on it or not?

**Team:** It was cool overall. I learned a couple of useful libraries for charting.

**ML Team:** I only worked on ML. I did the maximum backend work on the API and microservice, while other guys handled the frontend, other backend parts, and databases. Regarding ML, the impact was very positive. Gaining real experience was cool and interesting. It was also interesting to work in a situation where there was no existing foundation or research to rely on.

**Customer:** Yes. Well, your first stage is finished. Next year, perhaps you come up with your own ideas for what to do.

**Team:** Will we have clients?

**Customer:** No, I think you will have a choice, but the general idea is that you conceive and build something yourselves. If you have any wishes in the future to continue or do something, feel free to write. I am always open to collaboration.

**ML Team:** Is the project open source?

**Customer:** This part, yes.

**ML Team:** Regarding the specific training pipeline, I will share it after the course ends. I trained KS using one method, and many new innovations appeared in DT and DB. After the course presentation, I will likely push higher-quality pipelines for DT and DB to GitHub.

---

## Closing Remarks

### 00:28:00

**Customer:** Any other questions or topics to discuss? Probably no point in changing anything now anyway. Overall, good job, guys, well done. If it was interesting, that is the most important thing. If it was also useful, that is even better.

**Team:** Yes, yes. So, that is it?

**Customer:** Yes, let us wrap up. Have a good evening. Check everything, fix bugs, and let us know when it is ready.

**Team:** When everything is ready, I will write and send everything.

**Customer:** Yes, let us go. Good evening, bye-bye. Thanks for the work. Have a good day.

**Team:** Thank you too. Alright, bye.

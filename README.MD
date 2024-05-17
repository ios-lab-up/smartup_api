<div align="center">

# 🚀 SMARTUP-API 🚀

> 💡 Ultimate API that bridges the gap between your genius and UPSite. 💡

</div>

<div align="center">

## 🛠 Prerequisites 🛠

</div>

🔧 Gear up! Before you dive into the installation, make sure your system is armored with:

- **Docker Desktop 🐳**

> 📚 Installation Guides 📚

</div>

| 💻 Operating System |                                  📘 Guide                                  |
| :-----------------: | :-------------------------------------------------------------------------: |
|       Windows       | [Install on Windows](https://docs.docker.com/desktop/install/windows-install/) |
|        MacOS        |    [Install on MacOS](https://docs.docker.com/desktop/install/mac-install/)    |
|        Linux        |   [Install on Linux](https://docs.docker.com/desktop/install/linux-install/)   |

<div align="center">

## 🚦 Installation Steps 🚦

</div>

1. **Clone the Batmobile** 🦇

   > Ensure that your **Personal Access Token** or **SSH Key** is authorized to allow you full throttle on the git highway 🛣️.
   >

   ```sh
   $ git clone git@github.com:iOS-Lab-UP/SmartUP-API.git
   ```
2. **Rev the Engine** 🏎️

   > Once the repo is cloned, run this spell 🧙‍♂️ inside the project's root folder to summon the Docker container.
   >
   > ❗ **Caution:** May vary based on your operating system.
   >

   ```sh
   $ docker compose up
   ```

   🌟 Expect your terminal to light up like this when the spell takes effect 🌟

   ```plaintext
   UP_DB       | 2023-03-07T06:46:13.746712Z 0 [Note] Server hostname (bind-address): '0.0.0.0'; port: 3306
   UP_DB       | 2023-03-07T06:46:13.746746Z 0 [Note]   - '0.0.0.0' resolves to '0.0.0.0';
   UP_DB       | 2023-03-07T06:46:13.746764Z 0 [Note] Server socket created on IP: '0.0.0.0'.
   UP_DB       | 2023-03-07T06:46:13.748873Z 0 [Warning] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
   UP_DB       | 2023-03-07T06:46:13.752727Z 0 [Note] Event Scheduler: Loaded 0 events
   UP_DB       | 2023-03-07T06:46:13.752969Z 0 [Note] mysqld: ready for connections.
   UP_DB       | Version: '5.7.41'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
   ```
3. **Navigate the Stars** 🌌

   > Set sail to [http://localhost:5555/health_check](http://localhost:5555/health_check) on your trusty web-ship and behold the astral response!
   >

   ```json
   {
      "cpu_usage": "5.3%",
      "date": "2023-03-07 00:27:00",
      "memory_usage": "17.0%",
      "message": "Server is up and running",
      "port": 5555,
      "status": "OK",
      "uptime": "1.76 days"
   }
   ```
4. **Dock the Spaceship** 🚀

   > Use **CTRL-C** in the terminal to bring your spaceship back to the hangar. To erase the echoes of your journey, enter the following incantation:
   >
   > ❗ **Caution:** May vary based on your operating system.
   >

   ```sh
   $ docker compose down -v
   ```

<div align="center">

## 🎉 Conclusion 🎉

</div>

🏅 Congratulations, Space Explorer! You have successfully navigated the nebula of SmartUP-API container creation. 🌠

For any interstellar anomalies or troubleshooting, please transmit your signals to the galactic guardians! 🌌 @luisced, @maurch.

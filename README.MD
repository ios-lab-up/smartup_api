# SMARTUP-API

> UP API that connects to UPSite

## Prerequisites

Before you begin, you have shold have the following installed on your system:

- Docker Desktop

> Installation Guides:

| System                                                           |
| ---------------------------------------------------------------- |
| [Windows](https://docs.docker.com/desktop/install/windows-install/) |
| [MacOS](https://docs.docker.com/desktop/install/mac-install/)       |
| [Linux](https://docs.docker.com/desktop/install/linux-install/)     |

## Steps

1. Clone the SmartUP-API repo:

   > Make sure you already authorized your **Personal Acess Token** or your **SSH Key**, on order to be able to write.
   >

   `$ git clone git@github.com:iOS-Lab-UP/SmartUP-Web.git`
2. Once you've already cloned the repo, run the following command in order to start the container:

   > **Note:** This may vary depending on the OS you're using
   >

   `$ docker compose up`

   **You should be able to see a terminal output similar to this one, once the procces finished:**

```
UP_DB       | 2023-03-07T06:46:13.746712Z 0 [Note] Server hostname (bind-address): '0.0.0.0'; port: 3306
UP_DB       | 2023-03-07T06:46:13.746746Z 0 [Note]   - '0.0.0.0' resolves to '0.0.0.0';
UP_DB       | 2023-03-07T06:46:13.746764Z 0 [Note] Server socket created on IP: '0.0.0.0'.
UP_DB       | 2023-03-07T06:46:13.748873Z 0 [Warning] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
UP_DB       | 2023-03-07T06:46:13.752727Z 0 [Note] Event Scheduler: Loaded 0 events
UP_DB       | 2023-03-07T06:46:13.752969Z 0 [Note] mysqld: ready for connections.
UP_DB       | Version: '5.7.41'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
```


3. Acces the application in a web browser. In this example, you can acces the application by navigating to [http://localhost:5555/health_check](http://localhost:5555/health_check), where you should be able to watch a similar response:

```
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

4. To Stop the container, use **CTRL-C** in the twerminal where **docker compose up** is running, to delete all the data in the container volumes enter:

   > **Note:** This may vary depending on the OS you're using
   >

   `$ docker compose down -v`

   ## Conclusion

   Congratulations! You have succesfully built the SmartUP-API container. For any questions or troubleshooting, please contact the mantainers.

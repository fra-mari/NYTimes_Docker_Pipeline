<p align='center'><img src='./img_and_gif/NYTtopic_logo.png' height='110'></p>

<h1 align="center" >The New York Times Docker Pipeline</h1>

<p align="center"><img src="https://img.shields.io/badge/Made%20with-Python-E8B90F.svg"/> <img src="https://img.shields.io/badge/Maintained%5F-yes-pink.svg"/> <img src="https://img.shields.io/badge/Hosted-oh%20yes!-pass.svg"/> <img src="https://img.shields.io/badge/License-MIT-blue.svg"/><br></p><p align="center"><i>Available on Telegram <a href="https://t.me/NYTtopic_bot">@NYTtopic</a></i><br></p>



<br>

<div><div style="float: left; padding-right: 15px">
<img src='./img_and_gif/NYTtopic.gif' height='650' align='left'>
</div>This code maintains a simple <b>Telegram bot</b> which collects fresh updates from the Twitter account of <i>The New York Times</i> and allows the user to look for recent articles on topics of their choice.<br>Hosted on <a href='https://aws.amazon.com/ec2/'><b>Amazon EC2</b></a>, the <a href="https://t.me/NYTtopic_bot">NYTtopic Bot</a> consists of a pipeline of Docker containers:<br><br>
  <p>➤&nbsp;a <b>first container</b> runs a Python module which leverages <a href='https://www.tweepy.org'>Tweepy</a> for accessing <i>The New York Times</i>'s profile via the <a href='https://developer.twitter.com/en/docshttps://developer.twitter.com/en/docs'>Twitter API</a>, creating a stream of tweets and storing these into a <a href='https://www.mongodb.com/'>Mongo database</a> (<b>second container</b>);</p><br>
  <p>➤&nbsp;the <b>third container</b> carries out ETL tasks. It uses <a href='https://spacy.io'>SpaCy</a> to perform <a href='https://en.wikipedia.org/wiki/Named-entity_recognition'><b>named-entity recognition (NER)</b></a> on the text of each tweet extracted from MongoDB. These tags are then formatted as <i>#hashtags</i>, and all the data are eventually stored into a <a href='https://www.postgresql.org'>PostgreSQL database</a> (<b>fourth container</b>);</p><br><p>➤&nbsp;the <b>fifth container</b> feeds all the data into the Telegram bot, which is controlled and kept online using a library called <a href='https://python-telegram-bot.readthedocs.io/en/stable/'>Python Telegram Bot</a>.</p><br>I hope this bot will be useful anytime you are looking for high quality information.<br><br><br></div>




---

### Used Technology

<p>
<img src="https://img.shields.io/badge/aws-%23FC4C02.svg?&style=for-the-badge&logo=amazon%20aws&logoColor=white"height="24" /> <img src="https://img.shields.io/badge/docker-%232496ED.svg?&style=for-the-badge&logo=docker&logoColor=white" height="24"/> <img src="https://img.shields.io/badge/python-%233776AB.svg?&style=for-the-badge&logo=python&logoColor=white" height="24" /> <img src="https://img.shields.io/badge/mongodb-%2347A248.svg?&style=for-the-badge&logo=mongodb&logoColor=white"  height="24" /> <img src="https://img.shields.io/badge/postgresql-%23336791.svg?&style=for-the-badge&logo=postgresql&logoColor=white"  height="24" /> <img src="https://img.shields.io/badge/python–telegram–bot-%2326A5E4.svg?&style=for-the-badge&logo=telegram&logoColor=white" height="24"  /> <img src="https://img.shields.io/badge/tweepy-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" height="24" /> <img src="img_and_gif/SpaCy_logo.png" height="24"><br><br><b>Guest Star</b><br>
  <img src="https://img.shields.io/badge/The New York Times-%23333333.svg?&style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBpZD0iU3ZnanNTdmcxMDAxIiB3aWR0aD0iMjg4IiBoZWlnaHQ9IjI4OCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4bWxuczpzdmdqcz0iaHR0cDovL3N2Z2pzLmNvbS9zdmdqcyI+PGRlZnMgaWQ9IlN2Z2pzRGVmczEwMDIiPjwvZGVmcz48ZyBpZD0iU3ZnanNHMTAwOCIgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMSwwLDApIj48c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjI4OCIgaGVpZ2h0PSIyODgiIHZpZXdCb3g9IjAgMCAxMy45IDE4LjYiPjxwYXRoIGQ9Ik0xMy45LDIuNUMxMy45LjUsMTIsMCwxMC41LDBWLjNjLjksMCwxLjYuMywxLjYsMWExLjA1ODcyLDEuMDU4NzIsMCwwLDEtMS4yLDEsMTIuOTU4NTMsMTIuOTU4NTMsMCwwLDEtMy4zLS44QTEzLjI3NTI3LDEzLjI3NTI3LDAsMCwwLDQuMS43LDMuMjcwNDMsMy4yNzA0MywwLDAsMCwuNywzLjksMi4zMTc3NywyLjMxNzc3LDAsMCwwLDIuMiw2LjFsLjEtLjJhMS4wNTM4MSwxLjA1MzgxLDAsMCwxLS42LTFBMS4yNjU5MywxLjI2NTkzLDAsMCwxLDMuMSwzLjhhMTQuNzc2LDE0Ljc3NiwwLDAsMSwzLjcuOSwyOC4yNTc3MywyOC4yNTc3MywwLDAsMCwzLjcuOFY4LjZMOSw5LjlWMTBsMS41LDEuM3Y0LjNhNC42MTc5LDQuNjE3OSwwLDAsMS0yLjUuNiw0LjkyOTEzLDQuOTI5MTMsMCwwLDEtMy45LTEuNmw0LjEtMnYtN2wtNSwyLjJBNi42ODUxNSw2LjY4NTE1LDAsMCwxLDUuOCw0LjlsLS4xLS4yQTcuNDcxMzMsNy40NzEzMywwLDAsMCwwLDExLjZhNy4wMTk0OCw3LjAxOTQ4LDAsMCwwLDcsNyw2LjUwNTMyLDYuNTA1MzIsMCwwLDAsNi42LTYuNWgtLjJhNi42OTc0OCw2LjY5NzQ4LDAsMCwxLTIuNiwzLjFWMTEuMWwxLjYtMS4zVjkuN0wxMC45LDguNHYtM0EyLjg1NzkxLDIuODU3OTEsMCwwLDAsMTMuOSwyLjVabS04LjcsMTFMNCwxNC4xYTUuOTMyNDcsNS45MzI0NywwLDAsMS0xLjEtMy44LDcuMTA2NDcsNy4xMDY0NywwLDAsMSwuMy0yLjFsMi4xLS45WiIgZmlsbD0iI2ZmZmZmZiIgY2xhc3M9ImNvbG9yMDAwIHN2Z1NoYXBlIj48L3BhdGg+PC9zdmc+PC9nPjwvc3ZnPg==&logoColor=white" height="24" /></p>


---

### Instructions For Using This Code Locally

#### 📌&nbsp; STEP 1: Obtain credentials for the [Twitter API](https://developer.twitter.com/en/docshttps://developer.twitter.com/en/docs) and the [Telegram Bot API](https://core.telegram.org/bots/api)

- Open profiles on [Twitter](https://twitter.com/) and [Telegram](https://telegram.org/) if you do not already have them. 
- Four authentication keys are needed to access Twitter's Streaming API: **API Key**, **API Secret**, **Access Token** and **Access Token Secret**:
  - You can obtain them by registering an application on [apps.twitter.com](https://apps.twitter.com/).
  - Once in possession of the access keys, store them locally as _environment variables_ with the following names: `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `SECRET_ACCESS_TOKEN`.

- Authentication to Telegram Bot Api is coparatively easier, as you only need one **Access Token**:
  - To generate it, you have to chat with [BotFather](https://core.telegram.org/bots#6-botfather) on Telegram (no kidding!) and follow a few simple steps (to prevent overlapping, please make sure you do not choose [NYTtopic](https://t.me/NYTtopic_bot) as a name for your bot&nbsp;🙏🏻).
  - Once again, store the token as an _environment variable_. Call it `TOKEN_TELEGRAM`.

#### 📌&nbsp; STEP 2: Run the pipeline with Docker

- Clone this repository and install [Docker](https://www.docker.com/get-started) if needed.
- Go into the folder `NYTopic_twitter_to_telegram`:
  - run `docker-compose build` and wait for Docker to set up everything for you;
  - run `docker-compose up`. The bot should start responding within a few seconds.
- Open a Telegram chat with your new bot and start browsing *The New York Times*!

---

### To Do

- [ ] Add a container for removing old records from Mongo and Postgres.
- [ ] Provide the user with links to similar content in other newspapers.
- [ ] Make hashtag-based queries possible, so as to return all the articles related to a precise topic available in a single message.


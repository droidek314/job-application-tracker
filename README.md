# Automated Job Application Tracker

## About this project
This project is made for easier managing of all job applications that user can apply to. It is made with usability in mind first - it's main purpose is the almost full automation of tracking every application. Automatic updating of their statuses is achieved by optional Gmail inbox scanning for new letters with code words.

## Main functionality:
- Intuitive, responsive and fast interface
- Automatic parsing of the company name and job title from the given URL
- Optional Gmail inbox scanning to automatically check and update application statuses

## Technologies used:
- Python 3.10
- CustomTKinter
- BeautifulSoup4
- Google API
- SQLite3

## How to run this project locally:
If you want to run source code locally on your computer, follow these steps:
1. Clone this repository to any folder.
```bash
git clone https://github.com/droidek314/job-application-tracker
```
2. Open the folder.
```bash
cd job-application-tracker
```
3. Install all dependencies.
```bash
pip install -r requirements.txt
```
4. Run the main file.
```bash
python3 app.py
```

## Google API Setup (Gmail Integration)
To use the automatic Gmail scanning feature, you need to provide your own Google API credentials. Here is how to get them:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **New Project**.
3. Navigate to **APIs & Services > Library**, search for **Gmail API**, and click **Enable**.
4. Go to the **OAuth consent screen** and configure it. If you are just testing, set the user type to **External** and add your own email address to the "Test users" list.
5. Go to **Credentials**, click **Create Credentials**, and select **OAuth client ID**. Choose **Desktop app** as the application type.
6. Download the generated JSON file, rename it to `credentials.json`, and place it in the root directory of this project.

*Note: The very first time you run the app and use the scanning feature, it will open your web browser asking for permission to access your Gmail. Once granted, it will generate a `token.json` file locally so you won't have to log in every time.*

## About author
This project started rather as an educational initiative before it became a genuinely useful tool for me. The logic and the structure of the code were analyzed and implemented by me. While learning, understanding the best approaches and refactoring the code AI was used as a helping instrument, but not as the main source of this project's architecture.

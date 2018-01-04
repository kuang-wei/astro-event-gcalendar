# astro-event-gcalendar

This python program adds all upcoming [seminars/colloquia](http://astro.uchicago.edu/events/index.php) scheduled by the [Department of Astronomy & Astrophysics](http://astro.uchicago.edu) at the University of Chicago to your Google Calendar

Talk titles, dates, times, and room locations are all be automatically added

## Getting Started

These instructions will get you a copy of the project up and running on your local machine

### Prerequisites

* Python 2.6 or greater.
* The pip package management tool.
* Access to the internet and a web browser.
* A Google account with Google Calendar enabled.

### Installing

#### Step 0: Clone this repository
```
git clone https://github.com/kuang-wei/astro-event-gcalendar.git
```

#### Step 1: Turn on the Google Calendar API
1. Use [this wizard](https://console.developers.google.com/start/api?id=calendar) to create or select a project in the Google Developers Console and automatically turn on the API. Click **Continue**, then **Go to credentials**.
2. On the **Add credentials to your project** page, click the **Cancel** button.
3. At the top of the page, select the **OAuth consent screen** tab. Select an **Email address**, enter a **Product name** if not already set, and click the **Save** button.
4. Select the **Credentials** tab, click the **Create credentials** button and select **OAuth client ID**.
5. Select the application type **Other**, enter the name "Google Calendar API Quickstart", and click the **Create** button.
6. Click **OK** to dismiss the resulting dialog.
7. Click the &#xe2c4 (Download JSON) button to the right of the client ID.
8. Move this file to the cloned repository and rename it `client_secret.json`.

#### Step 2: Install the Google Client Library
Run the following command to install the library using pip:
```
pip install --upgrade google-api-python-client
```
See the library's [installation page](https://developers.google.com/api-client-library/python/start/installation) for the alternative installation options.


## Running the program

```
python create_event.py
```
As the program is adding events to your calendar, it will print out the details of the events in the following format:

```
------------------
TITLE
DATE-TIME
LOCATION
new event added/exisiting event updated
CALENDAR EVENT URL
------------------
```

## Authors

* **Kuang Wei** - <kuangwei@uchicago.edu>

## Acknowledgments

* User guide of the Google Calendar API
* Experienced developers on Stack Exchange
* Billie Thompson - [PurpleBooth](https://github.com/PurpleBooth) for the README template
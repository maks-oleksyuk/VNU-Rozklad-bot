# Telegram Bot to show university schedule

This is a Telegram bot for showing the university schedule,
with a user-friendly interface and the use of third-party APIs ([© ПП Політек-софт](http://www.politek-soft.kiev.ua/)).

## Instructions for launching the bot

To run the bot, you need to install dependencies and configure some environment variables.
Below are instructions on how to do this:

1. Clone the repository to your local computer:

    ``` sh
    git clone https://github.com/maks-oleksyuk/VNU-Rozklad-bot.git
    ```

2. Create an `.env` file in the root directory of the project
   and fill it according to the example specified in the `example.env` file

    ``` dotenv
    TOKEN=your_bot_token
    ADMIN_ID=1234567
    API_IP=0.0.0.0
    # and other, see example.env
    ```
3. If all the variables are configured correctly, you can run the bot on Docker.
   To do this, you can execute the following commands.

    ``` sh
    make build; make up
    ```

4. Import mariadb database. In order to import an existing database,
   you can place the `.sql` file in the `./db-init` folder for automatic import when the container is started

5. More detailed information can be obtained with the following command:

   ``` sh
   make help
   ```

## Commands

This Telegram bot has the following commands:

* `start`    - 🚀 Start the bot
* `now`      - 🔆 Current pair
* `today`    - ⬇️ Schedule for today
* `tomorrow` - ⤵️ Schedule for tomorrow
* `week`     - ⏬ Schedule for the week
* `nextweek` - ⏩ Schedule for next week
* `set_date` - 📆 Schedule for the entered date
* `about`    - ℹ️ About the bot
* `help`     - ❔ Help
* `cancel`   - 🆑 Cancel action | Change request

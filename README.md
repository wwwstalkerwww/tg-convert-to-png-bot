# tg-gemini-bot: WebP Sticker and Image to PNG Converter Bot

This Telegram bot is designed to convert WebP stickers and some other images to PNG format. It is useful when you need to get regular PNG images from stickers that Telegram sends as WebP by default.

## Features

* **WebP Sticker to PNG Conversion:** Converts stickers sent in Telegram as WebP to standard PNG images.
* **Some Image to PNG Conversion:** Supports conversion of some other image formats as well (please specify supported formats in the bot documentation, if available).
* **Ease of Use:** Easy to launch and use, both with Python and via Docker.

## How to Launch the Bot

### Method 1: Launching with Python

1. **Clone the repository (if applicable) or download the bot files.**
2. **Install dependencies:**
   Navigate to the bot directory and execute the command:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure you have installed all the necessary libraries listed in `requirements.txt`.

3. **Configure the bot token:**
   Open the `convert-bot_token.py` file and find the line `TOKEN = "YOU_BOT_TOKEN"`.
   Replace `"YOU_BOT_TOKEN"` with your Telegram bot token obtained from BotFather.

4. **Launch the bot:**
   Execute the command:
   ```bash
   python convert-bot_token.py
   ```
   The bot should start and be ready to work in Telegram.

### Method 2: Launching with Docker

1. **Install Docker and Docker Compose (if not installed).**
2. **Build the Docker image:**
   Navigate to the directory with `Dockerfile` and execute the command:
   ```bash
   docker build -t convert-bot .
   ```
   This command will create a Docker image named `convert-bot` based on the `convert-bot.dockerfile` file (which uses `convert-bot.py`).

3. **Run the Docker container:**
   Run the container, specifying the bot token as an environment variable. Replace `<YOUR_BOT_TOKEN>` with your actual token:
   ```bash
   docker run -d --name convert-bot-container -e TOKEN=<YOUR_BOT_TOKEN> convert-bot
   ```
   * `-d` - run in detached mode (background mode).
   * `--name convert-bot-container` - container name (you can choose another).
   * `-e TOKEN=<YOUR_BOT_TOKEN>` - passing the bot token as an environment variable.

   **Or, if you are using `docker-compose.yml` (recommended):**
   Create a `docker-compose.yml` file (if you don't have one) with the following example content:
   ```yaml
   version: '3.8'
   services:
     convert-bot:
       build: .
       environment:
         TOKEN: <YOUR_BOT_TOKEN>
       restart: always # Restart the container in case of an error
   ```
   Replace `<YOUR_BOT_TOKEN>` with your token.
   Then run the command:
   ```bash
   docker-compose up -d --build
   ```

### Launching from a Ready-Made Docker Image (convert-bot.tar)

The `convert-bot.tar` file can be used to unpack the image in Docker. This is usually required in more complex scenarios or when transferring an image. If the standard build method via `docker build` works correctly, using `convert-bot.tar` may not be necessary.

**If you need to use `convert-bot.tar` (example process):**

1. **Upload `convert-bot.tar` to the server where Docker is running.**
2. **Load the image from the tar archive:**
   ```bash
   docker load -i convert-bot.tar
   ```
   This command will load the image into the local Docker repository.
3. **Run the container as described in the "Run the Docker container" section above**, using the image name that was loaded from the tar archive.

## Required Dependencies

Make sure you have installed all the dependencies listed in the `requirements.txt` file. This can usually be done with the command:
```bash
pip install -r requirements.txt
```
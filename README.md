# Discord Boost Bot 🚀

A powerful and feature-rich Discord bot designed for server boosting, key management, and automation. Built with performance and customization in mind, this bot is perfect for server administrators and service providers looking to enhance their Discord communities with ease. 🌟

---

## 📖 Overview

The **Discord Boost Bot** is a professional tool that automates server boosting, manages boost keys, and provides a seamless user experience with rich embeds, webhook logging, and captcha-solving capabilities. Whether you're boosting servers manually or running an automated service, this bot has everything you need to streamline the process. 💻

---

## ✨ Key Features

- **Server Boosting** ⚡: Boost Discord servers with 1-month or 3-month Nitro tokens using a simple command.
- **Key Management** 🔑: Create, manage, and track boost keys with detailed statistics and filtering options.
- **Auto-Boosting** 🤖: Automate boosting with configurable intervals and error handling.
- **Captcha Solving** 🛡️: Supports multiple captcha services (hCaptcha, Capsolver, etc.) to bypass rate limits.
- **Rich Presence** 🎮: Customizable bot status with activities like playing, streaming, or listening.
- **Webhook Logging** 📡: Send detailed boost logs to a Discord webhook for real-time monitoring.
- **Proxy Support** 🌐: Use proxies to enhance security and bypass restrictions.
- **Customizable UI** 🎨: Beautiful embeds with success, error, and info states, plus customizable thumbnails and bios.
- **Robust Error Handling** 🛠️: Comprehensive error management to ensure smooth operation.
- **Token Stock Management** 📦: Easily add, view, and remove tokens from stock files.

---

## 📋 Prerequisites

Before setting up the bot, ensure you have the following:

### System Requirements
- **Operating Systems**: Windows, macOS, or Linux 🖥️
- **Python Version**: Python 3.8 or higher 🐍
- **Disk Space**: At least 500 MB for dependencies and data files 💾
- **Internet Connection**: Stable connection for API calls and Discord interactions 🌍

### Required Tools
- **Python**: Install from [python.org](https://www.python.org/downloads/) or your package manager.
- **Git**: For cloning the repository (optional).
- **pip**: Python package manager (comes with Python).

### Required Accounts
- **Discord Bot Token**: Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications) and enable all intents.
- **Captcha Solver API Key** (optional): For services like hCaptcha or Capsolver.
- **Webhook URL** (optional): For logging boost activities to a Discord channel.

---

## 🛠️ Installation

Follow these steps to get the bot up and running:

1. **Clone the Repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd discord-boost-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:
   - Open `config/config.json` and fill in:
     - `bot.token`: Your Discord bot token.
     - `webhook.url`: Your Discord webhook URL (optional).
     - `captcha_solver`: API keys for captcha services (optional).
     - Other settings like `customization`, `auto_config`, etc., as needed.
   - Edit `config/onliner.json` to customize bot presence (e.g., status, activities).
   - Add Nitro tokens to `data/1m.txt` (1-month) or `data/3m.txt` (3-month).
   - Add proxies to `data/proxies.txt` (optional).

4. **Run the Bot**:
   ```bash
   python run.py
   ```

5. **Invite the Bot**:
   - Invite the bot to your Discord server using the link generated in the Discord Developer Portal.
   - Ensure the bot has the necessary permissions (e.g., `Send Messages`, `Embed Links`).

---

## 🚀 Usage

Once the bot is running, you can interact with it using slash commands or the configured prefix (default: `,`).

### Available Commands
| Command                     | Description                                         | Example                     |
|-----------------------------|-----------------------------------------------------|-----------------------------|
| `/boost`                    | Boost a server with tokens.                         | `/boost`                    |
| `/new_keys`                 | Create new keys for boosting.                       | `/new_keys`                 |
| `/get_all_keys`             | Retrieve all keys in the system.                    | `/get_all_keys`             |
| `/get_keys`                 | Filter keys by month and amount.                    | `/get_keys`                 |
| `/delete_keys`              | Delete keys from the system.                        | `/delete_keys 1 2 10`       |
| `/get_key_information`      | Get details about a specific key.                   | `/get_key_information <key>`|
| `/key_stats`                | Show key statistics.                                | `/key_stats`                |
| `/get_used_key_information` | Get details about a used key.                       | `/get_used_key_information <key>` |
| `/get_key`                  | Retrieve a key by month and amount.                 | `/get_key 1 2`              |
| `/delete_key`               | Delete a specific key.                              | `/delete_key <key>`         |
| `/add_stock`                | Add tokens to stock.                                | `/add_stock 1 <tokens>`     |
| `/view_stock`               | View current token stock.                           | `/view_stock`               |
| `/remove_stock`             | Remove tokens from stock.                           | `/remove_stock 1 5`         |
| `/start_auto_boost`         | Start the auto-boosting service.                    | `/start_auto_boost`         |
| `/stop_auto_boost`          | Stop the auto-boosting service.                     | `/stop_auto_boost`          |
| `/auto_boost_status`        | Check the auto-boosting status.                     | `/auto_boost_status`        |

### Example Workflow
1. Add tokens to stock:
   ```bash
   /add_stock 1 <token1>\n<token2>
   ```
2. Boost a server:
   ```bash
   /boost
   # Follow the modal to enter invite, amount, and months
   ```
3. Start auto-boosting:
   ```bash
   /start_auto_boost
   ```

---

## 🖼️ Screenshots

*(You can add screenshots of the bot's embeds, console output, or command interactions here by uploading images to the repository and linking them.)*

- **Boost Success Embed**: A vibrant green embed showing successful boosts. ✅
- **Error Handling**: Clear red embeds for invalid inputs or errors. 🚫
- **Console Output**: Colorful logs with timestamps and status updates. 🖥️

---

## 🔧 Configuration

The bot is highly configurable through JSON files:

### `config.json`
- **Bot Settings**: Token, prefix, and status (e.g., `playing`, `streaming`).
- **Customization**: Thumbnail, bio, nickname for boosted accounts.
- **Auto-Boosting**: Default invite, retry limits, and intervals.
- **Captcha Solver**: API keys for hCaptcha, Capsolver, etc.
- **Webhook**: URL for logging boost activities.
- **Permissions**: Owner IDs and admin role IDs.

### `onliner.json`
- **Presence**: Customize bot status (e.g., `online`, `dnd`) and activities (e.g., `playing Minecraft`, `streaming on Twitch`).
- **Token Paths**: Specify files containing tokens for online status.

### Data Files
- `data/1m.txt` & `data/3m.txt`: Store Nitro tokens for boosting.
- `data/proxies.txt`: List of proxies in `http://user:pass@host:port` format.
- `data/keys/keys.json`: Store generated keys.
- `data/output/success.txt` & `data/output/failed_boosts.txt`: Log successful and failed boosts.

---

## 🛡️ Security

- **Proxies**: Use proxies to protect your IP and bypass rate limits.
- **Captcha Solving**: Automate captcha challenges with trusted services.
- **Error Handling**: Robust checks to prevent crashes and log issues.
- **Permissions**: Restrict commands to owners and admin roles.

---

## 🌐 Compatibility

The bot is compatible with:
- **Windows**: Windows 10 or later.
- **macOS**: macOS 10.15 (Catalina) or later.
- **Linux**: Most distributions (e.g., Ubuntu, Debian, CentOS).
- **Hosting**: Can be hosted on VPS or cloud services like AWS, Google Cloud, or Heroku.

---

## 📦 Dependencies

The bot relies on the following Python libraries (listed in `requirements.txt`):
- `discord.py`: For Discord API interactions.
- `colorama`: For colorful console logs.
- `httpx` & `tls-client`: For HTTP requests and fingerprinting.
- `fastapi` & `uvicorn`: For auto-boosting server.
- `websockets`: For onliner WebSocket connections.
- And more (see `requirements.txt` for the full list).

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows the project's style guidelines and includes tests where applicable. 🙌

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- **Discord.py Community**: For an amazing library and support.
- **Contributors**: Thanks to everyone who tests and improves the bot!

---

## 📬 Contact

For questions, suggestions, or support:
- **Discord**: Join our support server (configure in `config.json`).
- **Issues**: Open an issue on the repository.

Happy boosting! 🎉
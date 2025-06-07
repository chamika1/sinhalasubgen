# Multi-API Subtitle Translator (SinhalaSubGen)

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/chamika1/sinhalasubgen)](https://github.com/chamika1/sinhalasubgen/issues)
[![GitHub stars](https://img.shields.io/github/stars/chamika1/sinhalasubgen)](https://github.com/chamika1/sinhalasubgen/stargazers)

**Fast & Efficient English to Sinhala Subtitle Translation using Multiple Google Gemini API Keys.**

This application provides a user-friendly interface built with Tkinter to translate English SRT subtitle files into Sinhala. It leverages multiple Google Generative AI (Gemini) API keys for faster processing and resilience against rate limits.

## ✨ Features

*   **Multi-API Key Support:** Rotate through multiple API keys to maximize translation speed and avoid rate limits.
*   **Batch Processing:** Translates subtitles in batches for improved efficiency.
*   **Retry Mechanism:** Automatically retries failed batches.
*   **User-Friendly Interface:** Simple GUI for selecting input/output files and monitoring progress.
*   **Real-time Logging:** View translation progress and any issues in the log window.
*   **Customizable Batch Size:** Adjust the number of subtitles processed per API call.
*   **Auto API Key Rotation:** Option to enable or disable automatic switching between API keys.
*   **Progress Bar & Speed Indicator:** Track the translation progress and current speed.
*   **UTF-8 Support:** Ensures correct handling of Sinhala characters.
*   **Glittering Title Effect:** A visually appealing animated title.
*   **Sinhala Font Detection:** Attempts to use available Sinhala fonts for better display.

## 🖼️ Screenshot (Conceptual)

*(Imagine a screenshot of the application GUI here. You can add one to your repository!)*

## ⚙️ Requirements

*   Python 3.x
*   `google-generativeai` library

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chamika1/sinhalasubgen.git
    cd sinhalasubgen
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Open `app.py` and replace the placeholder API keys in the `self.api_keys` list with your own Google Gemini API keys:
    ```python
    self.api_keys = [
        "YOUR_API_KEY_1",
        "YOUR_API_KEY_2",
        "YOUR_API_KEY_3",
        # Add more keys if needed
    ]
    ```

## 📖 Usage

1.  Run the application:
    ```bash
    python app.py
    ```
2.  **Select Input File:** Click "Browse" next to "English Subtitle File (.srt)" and choose your English SRT file.
3.  **Output File (Optional):** The output file name will be auto-generated. You can change it by clicking "Browse" next to "Output Sinhala Subtitle File".
4.  **Adjust Settings (Optional):**
    *   **Batch Size:** Set the number of subtitle lines to process in each batch.
    *   **Auto API Key Rotation:** Check/uncheck to enable/disable automatic API key switching.
5.  **Start Translation:** Click "🚀 Start Fast Translation".
6.  **Monitor Progress:** Observe the progress bar, status messages, and log area.
7.  **Stop Translation (Optional):** Click "⏹️ Stop" if you need to interrupt the process.
8.  Once completed, the translated Sinhala SRT file will be saved to the specified location.

## 🛠️ How It Works

1.  **Parse SRT:** The input SRT file is parsed to extract individual subtitle entries (index, timestamp, text).
2.  **Create Batches:** Subtitles are grouped into batches based on the configured batch size.
3.  **Translate Batches:**
    *   Each batch is sent to the Google Gemini API for translation.
    *   The application rotates through the provided API keys to distribute the load and avoid rate limits.
    *   If an API call fails (e.g., due to rate limiting), it retries with the next key or after a delay.
4.  **Parse Response:** The API's response (translated text) is parsed.
5.  **Save Output:** The translated subtitles are compiled into a new SRT file, ensuring correct UTF-8 encoding for Sinhala characters.

## 🤝 Contributing

Contributions are welcome! If you have suggestions or find bugs, please open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (though you'll need to create this file if you want one).

## 📧 Contact

Rasanjana Chamika - [rasanjanachamika@gmail.com](mailto:rasanjanachamika@gmail.com)

Project Link: [https://github.com/chamika1/sinhalasubgen](https://github.com/chamika1/sinhalasubgen)

---

*This README was generated with assistance from an AI tool.*

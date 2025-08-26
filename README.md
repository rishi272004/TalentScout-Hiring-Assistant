# TalentScout Hiring Assistant Chatbot

## Overview
TalentScout Hiring Assistant is an AI-powered chatbot built with Streamlit that helps technology recruiters by automating the initial candidate screening process. The chatbot collects essential candidate information and generates tailored technical questions based on the candidate’s declared tech stack.

## Features
- Intuitive, form-based UI to gather candidate details.
- Dynamic technical question generation tailored to programming languages/frameworks/tools.
- Context-aware and coherent conversation flow.
- Multilingual support with auto language detection and translation.
- Sentiment analysis for personalized user interactions.
- Data handling compliant with GDPR using simulated anonymized storage.

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/TalentScout-Hiring-Assistant.git
cd TalentScout-Hiring-Assistant


2. Install dependencies:
pip install -r requirements.txt


3. Run the application locally:
streamlit run app.py


## Usage

1. Fill in your candidate information form.
2. Proceed to answer the technical questions generated based on your tech stack.
3. Submit your answers, and your data will be securely stored for recruiter review.
4. To end the interaction, you can type exit keywords or finish the interview in the UI.

## Technical Details

- Developed in Python using Streamlit for the frontend.
- Uses `langdetect` and `deep-translator` for language detection and translation.
- Sentiment analysis implemented via `TextBlob`.
- Modular design with clear separation of concerns:
- Prompt Engineering
- Context Management
- Multilingual Support
- Sentiment Analysis
- Data Handling

## Challenges & Solutions

- Overcame Python 3.13 compatibility issues with translation libraries by switching to `deep-translator`.
- Managed multi-language user inputs without disrupting the flow.
- Maintained conversation context and state persistence to prevent data loss on UI reruns.
- Designed flexible prompt engineering to handle multiple diverse tech stacks.

## Demo

(https://drive.google.com/file/d/1tRmOhGzw1FXU9WNrIbUGMhh6KoSkhb0R/view?usp=sharing)

## Deployment

You can deploy this app easily on **Streamlit Community Cloud**:

1. Push your code to a **public GitHub repository**.
2. Log in to [streamlit.io/cloud](https://streamlit.io/cloud).
3. Create a new app linked to your GitHub repo.
4. Set `app.py` as the main file.
5. Deploy and share.

Other deployment options include Heroku, AWS, or GCP.

## Contact

For questions or issues, contact: your-email@example.com

---

*Thank you for trying out the TalentScout Hiring Assistant!*


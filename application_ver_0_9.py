import openai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time
from flask import Flask, render_template_string, request, redirect
import threading
import html
import re

#Call Connected Python Files:
import HTML_Templates as HTML_Templates

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "### INSERT API KEY HERE ###"

# Call sample HTML templates, and example prompts
sample_html_template = HTML_Templates.TEMPLATES["template_1"]
previous_html_prompt = HTML_Templates.previous_html_prompt

# Store generated templates and content
current_html_template = sample_html_template
final_email_content = ""
final_combined_email = ""
previous_email_prompt = ""
image_url = ""
background_image_url = ""
custom_image_prompt = ""
custom_background_prompt = ""
keywords_memory = []
use_keyword_summary = False  # New flag to control repetitive content prevention
background_usage = "body"

# Variables for authentication and model configuration
defined_api_key = ""
defined_email = ""
defined_password = ""

#Did not connected to functions yet!!!!!!!!!!
generate_html_template_model = "gpt-3.5-turbo"
generate_email_content_model = "gpt-4"
merge_html_and_content_via_llm_model = "gpt-3.5-turbo"
generate_summary_keyword_model = "gpt-4"

# Function to generate HTML email template
def generate_html_template(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an HTML designer tasked with editing and improving email templates.
                            Make modifications according to the user's detailed instructions. Do not make any additinal changes, unless its told you to do so.
                            Do not touch to any placeholder text (lorem ipsum) in the template, unless its told you to do so.
                            Set body buttons and footer buttons seperately; if a body button specified used it in the body, if a footer link specified used it in the footer.
                            Ensure the content remains professional and adheres to best practices for HTML email design. 
                            Only return the updated HTML without any additional explanations or comments."""
            },
            {
                "role": "user",
                "content": f"The following is a sample HTML template. Please modify it based on the user's requirements:\n\n{sample_html_template}\n\n"
                           f"Here are the requested changes or updates:\n\n{prompt}"
            }
        ],
        max_tokens=1500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Function to generate plain text email content
def generate_email_content(prompt, presence_penalty_value=0, frequency_penalty_value=0):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": (
                    """You are an expert content writer tasked with generating high-quality, informative email content.
                    The content should be structured, engaging, and tailored to the given topic.
                    Ensure the content contains one main header (as 'Subject:'), and use subheaders where necessary to organize the information logically.
                    Ensure the content is complete, covering the main idea thoroughly but concisely.
                    Do not include any formatting or HTML tags.
                    The tone should match the context. 
                    Use a friendly and motivational tone for inspirational messages.
                    Use a clear and concise tone for tutorials.
                    Informative tone for educational concepts.
                    For customer relationship management (CRM) content, use a friendly, professional, and personalized tone to engage the customer.
                    Try to generate responses without using any placeholder text like [Recipient's Name], [Your Name], or [Company Name].
                    If signing an email, use 'mailmancer AI'.
                    If writing content on behalf of someone else, use '[Company Name]' or '[Your Name]' accordingly, do not use 'mailmancer AI' in this case.
                    Here are some examples of the type of content you might generate:
                    - Teaching an A1 English word: Include the word, its definition, an example sentence, and a pronunciation guide.
                    - Python tutorial: Explain the concept, provide a code example, and give a practical use case.
                    - Motivational message: Include an inspirational quote, followed by an explanation or actionable advice.
                    - Theoretical concept: Provide a definition, explain the key points, and include a real-world example.
                    - Christmas message to customers: Write a warm, festive message to customers and wishing them a happy holiday season.
                    - CRM content: Include personalized greetings, details about promotions or events, and a call to action to enhance customer engagement."""
                )
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
        presence_penalty=presence_penalty_value,
        frequency_penalty=frequency_penalty_value
    )
    return response.choices[0].message.content.strip()

# Function to generate an image from email content or custom prompt
def generate_email_image(email_content):
    summary_keyword = generate_summary_keyword(email_content, 1)
    image_prompt = f"""{summary_keyword}, stylized, animated depiction, resembling cartoon.
                        Focus on specific, visually representable elements.
                        Describe actions and scenarios rather than abstract concepts.
                        Avoid ambiguous language that could be interpreted as including text."""
                      
    dalle_response = openai.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        n=1,
        quality="standard",
        size="1024x1024"
    )
    return dalle_response.data[0].url


# Function to generate a background image from email content or custom prompt
def generate_background_image(email_content):
    summary_keyword = generate_summary_keyword(email_content, 1)
    image_prompt = f"""Create a soft, abstract background image that captures the essence of the following theme: '{summary_keyword}'. 
                    The colors should be subtle, calming, and suitable for use as an unobtrusive email background. Avoid using any text or specific recognizable objects; 
                    focus on creating an ambient atmosphere that enhances the visual experience without distracting from the main content."""

    dalle_response = openai.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        n=1,
        quality="standard",
        size="1024x1792"
    )
    return dalle_response.data[0].url


# Function to merge HTML and content
def merge_html_and_content_via_llm(html_template, email_content, image_url, background_image_url, background_usage):
    try:
        background_style = ""
        if background_usage == "body":
            background_style = "Apply background to email body background i.e. behind the container."
        elif background_usage == "container":
            background_style = "Apply background to email container background."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"""You are a skilled web developer and email designer. Your task is to merge a provided plain text content, body image, and background image into an HTML email template.
                        Here are your instructions:
                        1. Replace placeholders or sample text in the provided HTML template with the plain text content, preserving the HTML structure and styles.
                        2. Extract the subject from the text and use as header. The rest of the text should be included in the body **without omission**.
                        3. Apply one line of spacing at the beggining of body text content.
                        3. Retain styles, colors, alignment, and formatting defined in the HTML Template.
                        4. Retain the text alignment in the body. Do not apply any alignment to body by yourself.
                        5. If italic or bold format given in Plain Text Content, keep this formatting.
                        6. You can use bullet points only if its given in Plain Text Content. 
                        7. **Apply the same alignment of the rest of the body to bullets**. Avoid using large indentations for bullets.
                        8. **Do not forget to use every word in the Plain Text Content given to you.**
                        9. Replace the placeholder image URL in the body section of HTML Template with the provided 'Image URL'.
                        10. {background_style}
                        11. Maintain a clean and professional layout.
                        12. Output **only the resulting HTML content**. Do not include additional text or explanations before or after the HTML."""
                    )
                },
                {
                    "role": "user",
                    "content": f"HTML Template:\n{html_template}\n\nPlain Text Content:\n{email_content}\n\nImage URL:\n{image_url}\n\nBackground URL:\n{background_image_url}"
                }
            ],
            max_tokens=1800,
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        if not result.startswith("<!DOCTYPE html>"):  # Basic check for valid HTML
            raise ValueError("The response does not include valid HTML.")
        return result
    except Exception as e:
        print(f"Error in merging HTML and content: {e}")
        return "<!DOCTYPE html><html><body><p>Error generating HTML content.</p></body></html>"

# Function to truncate prompts
def truncate_prompt(prompt, max_length=200):
    if len(prompt) > max_length:
        return prompt[:max_length]
    return prompt
    
# Function to generate a summary keyword from generated email content
def generate_summary_keyword(email_content, n_key=1):
    truncated_content = truncate_prompt(email_content, max_length=200)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": (
                    f"""You are an assistant that summarizes email content into only {n_key} highly relevant keyword.
                        The keyword should represent the core theme or distinctive aspects of the content.
                        It should be brief, specific, and directly related to the main idea.
                        Only return the keyword, without any additional text or explanation.
                        Here are some examples of good summary keywords:
                        - Content about a shop or business: the type of shop or business concerned, e.g., 'bakery', or 'stationery'
                        - Content about a specific product of a shop or business: the name or concept of product concerned: e.g.,'TV', or 'pen'.
                        - Content about a new product launch: 'innovation', or 'product name'
                        - Content about a christmas holiday message: 'christmas', or 'holiday'
                        - Content about stress management techniques: 'stress relief', or 'mindfulness'
                        - Content about a Python tutorial: the specific Python concept or function being taught, e.g., 'Python loops', or 'for loop'
                        - Content about learning a new English word: the English word being taught, e.g., 'friend', or 'family'
                        - Content about explaining a theoretical concept: the concept being explained, e.g., 'supply and demand', or 'Bayes theorem'"""
                )
            },
            {"role": "user", "content": truncated_content}
        ],
        max_tokens=15,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# Function to extract email subject via regex:
def extract_subject_or_header(text):
    # Regular expressions to capture the subject or header
    subject_pattern = r'Subject: (.*)'
    header_pattern = r'Header: (.*)'

    # Search for the subject in the text
    subject_match = re.search(subject_pattern, text)

    if subject_match:
        return subject_match.group(1)
    else:
        # Search for the header in the text if subject is not found
        header_match = re.search(header_pattern, text)
        if header_match:
            return header_match.group(1)
    
    # Return None if neither Subject nor Header is found
    return None

def send_email(subject, body, to_email, cc_emails=None, bcc_emails=None):
    from_email = "### INSERT EMAIL HERE ###"
    email_password = "### INSERT PASSWORD HERE ###"

    # Create the email
    msg = MIMEText(body, "html")  # Specify that the content is HTML
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    if cc_emails:
        msg['Cc'] = cc_emails

    recipients = [to_email]
    if cc_emails:
        recipients.extend(cc_emails.split(","))
    if bcc_emails:
        recipients.extend(bcc_emails.split(","))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, email_password)
        server.sendmail(from_email, recipients, msg.as_string())


# Function to schedule sending emails at regular intervals
def schedule_regular_emails(interval_minutes, subject, prompt, to_email, cc_emails=None, bcc_emails=None, presence_penalty_value=0, frequency_penalty_value=0):
    def email_scheduler():
        while True:
            global final_email_content, final_combined_email, keywords_memory, use_keyword_summary
            # Generate new content
            if use_keyword_summary:
                summary_keyword = generate_summary_keyword(final_email_content)
                keywords_memory.append(summary_keyword)
            new_prompt = prompt + "\nAvoid using the following keywords, if and only if it doesn't prevent you from producing relevant content: " + ", ".join(keywords_memory)
            final_email_content = generate_email_content(new_prompt, presence_penalty_value=presence_penalty_value, frequency_penalty_value=frequency_penalty_value)
            # Generate new image based on the previous email prompt
            image_url = generate_email_image(final_email_content)
            # Merge the email content and HTML template
            final_combined_email = merge_html_and_content_via_llm(current_html_template, final_email_content, image_url, background_image_url, background_usage)
            # Send email
            send_email(extract_subject_or_header(final_email_content), final_combined_email, to_email, cc_emails, bcc_emails)
            time.sleep(interval_minutes * 60)
    # Start email scheduler in a separate thread
    threading.Thread(target=email_scheduler, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    global current_html_template, final_email_content, final_combined_email, image_url, background_image_url, custom_image_prompt, custom_background_prompt
    global previous_html_prompt, previous_email_prompt, sample_html_template, use_keyword_summary
    global defined_api_key, defined_email, defined_password
    global generate_html_template_model, generate_email_content_model, merge_html_and_content_via_llm_model, generate_summary_keyword_model, background_usage

    message = ""
    rendered_html_preview = current_html_template  # Rendered HTML tied to Step 1 only

    if request.method == "POST":
        action = request.form.get("action")

        if action == "Login":
            defined_api_key = request.form.get("api_key")
            defined_email = request.form.get("email")
            defined_password = request.form.get("password")
            message = "Logged in successfully." if defined_api_key and defined_email and defined_password else "Please enter all credentials."

        elif action == "Logout":
            defined_api_key = ""
            defined_email = ""
            defined_password = ""
            message = "Logged out successfully."

        elif action == "Configure Model":
            generate_html_template_model = request.form.get("generate_html_template_model")
            generate_email_content_model = request.form.get("generate_email_content_model")
            merge_html_and_content_via_llm_model = request.form.get("merge_html_and_content_via_llm_model")
            generate_summary_keyword_model = request.form.get("generate_summary_keyword_model")
            message = "Model configuration updated successfully."

        elif action == "Generate HTML Template":
            prompt = request.form.get("html_prompt")
            if prompt:
                previous_html_prompt = prompt
                current_html_template = generate_html_template(prompt)
                rendered_html_preview = current_html_template  # Update preview with generated template
                message = "HTML template generated successfully."
            else:
                message = "Please enter a prompt for the HTML template."

        elif action == "Generate Final Email Content":
            prompt = request.form.get("email_prompt")
            if prompt:
                previous_email_prompt = prompt
                final_email_content = generate_email_content(prompt)
                message = "Email content generated successfully."
            else:
                message = "Please enter a prompt for the email content."

        elif action == "Save Email Content Changes":
            edited_content = request.form.get("current_email_content")
            if edited_content:
                final_email_content = edited_content
                message = "Email content updated successfully."
            else:
                message = "Please enter content to save."

        elif action == "Save Combined HTML Changes":
            edited_combined_html = request.form.get("combined_html_content")
            if edited_combined_html:
                final_combined_email = edited_combined_html
                message = "Combined email HTML updated successfully."
            else:
                message = "Please enter content to save."

        elif action == "Generate Email Image":
            use_custom_prompt = request.form.get("use_custom_prompt")
            if use_custom_prompt == "yes":
                custom_prompt = request.form.get("custom_image_prompt")
                if custom_prompt:
                    custom_image_prompt = custom_prompt
                    image_url = generate_email_image(custom_prompt)
                    message = "Email image generated successfully using custom prompt."
                else:
                    message = "Please enter a custom prompt for the image."
            else:
                if final_email_content:
                    image_url = generate_email_image(final_email_content)
                    message = "Email image generated successfully using email content."
                else:
                    message = "Please generate the email content first."

        elif action == "Generate Background Image":
            use_custom_prompt = request.form.get("use_custom_background_prompt")
            if use_custom_prompt == "yes":
                custom_background_prompt = request.form.get("custom_background_prompt")
                if custom_background_prompt:
                    background_image_url = generate_background_image(custom_background_prompt)
                    message = "Background image generated successfully using custom prompt."
                else:
                    message = "Please enter a custom prompt for the background image."
            else:
                if final_email_content:
                    background_image_url = generate_background_image(final_email_content)
                    message = "Background image generated successfully using email content."
                else:
                    message = "Please generate the email content first."
            # Save the background usage selection
            background_usage = request.form.get("background_usage", "body")

        elif action == "Generate Combined Email Preview":
            # Get the user's selection for background usage
            background_usage = request.form.get("background_usage", "body")
            
            if current_html_template and final_email_content:
                if not image_url:
                    image_url = generate_email_image(final_email_content)
                
                # Call the function with the selected background usage
                final_combined_email = merge_html_and_content_via_llm(
                    current_html_template,
                    final_email_content,
                    image_url,
                    background_image_url,
                    background_usage
                )
                message = f"Combined email preview generated successfully with '{background_usage}' background."
            else:
                message = "Please ensure both the HTML template and email content are generated first."

        elif action == "Save Image URL":
            new_image_url = request.form.get("image_url")
            if new_image_url:
                image_url = new_image_url
                message = "Image URL updated successfully."
            else:
                message = "Please enter a valid image URL to save."

        elif action == "Save Background Image URL":
            new_background_image_url = request.form.get("background_image_url")
            if new_background_image_url:
                background_image_url = new_background_image_url
                message = "Background image URL updated successfully."
            else:
                message = "Please enter a valid background image URL to save."

        elif action == "Template 1":
            sample_html_template = HTML_Templates.TEMPLATES.get("template_1")
            if sample_html_template:
                current_html_template = sample_html_template
                rendered_html_preview = current_html_template
                message = "Template 1 selected."
            else:
                message = "Template 1 not found."

        elif action == "Template 2":
            sample_html_template = HTML_Templates.TEMPLATES.get("template_2")
            if sample_html_template:
                current_html_template = sample_html_template
                rendered_html_preview = current_html_template
                message = "Template 2 selected."
            else:
                message = "Template 2 not found."

        elif action == "Template 3":
            sample_html_template = HTML_Templates.TEMPLATES.get("template_3")
            if sample_html_template:
                current_html_template = sample_html_template
                rendered_html_preview = current_html_template
                message = "Template 3 selected."
            else:
                message = "Template 3 not found."

        elif action == "Add Template":
            custom_template = request.form.get("custom_template")
            if custom_template:
                sample_html_template = custom_template
                current_html_template = sample_html_template
                rendered_html_preview = current_html_template
                message = "Custom template added successfully."
            else:
                message = "Please enter a custom template."

        elif action == "Send Email":
            recipient = request.form.get("recipient")
            cc = request.form.get("cc")
            bcc = request.form.get("bcc")
            subject = request.form.get("email_subject", extract_subject_or_header(final_email_content) or "Generated Email")
            send_option = request.form.get("send_option")
            use_keyword_summary = request.form.get("use_keyword_summary") == "yes"
            use_presence_penalty = request.form.get("use_presence_penalty") == "yes"
            use_frequency_penalty = request.form.get("use_frequency_penalty") == "yes"
            presence_penalty_value = float(request.form.get("presence_penalty_value", 1)) if use_presence_penalty else 0
            frequency_penalty_value = float(request.form.get("frequency_penalty_value", 1)) if use_frequency_penalty else 0

            if recipient:
                if send_option == "One-Time Only":
                    send_email(subject, final_combined_email, recipient, cc, bcc)
                    message = "Email sent successfully."
                elif send_option == "Send at Regular Intervals":
                    interval = int(request.form.get("interval", "60"))  # Default to 60 minutes if not specified
                    schedule_regular_emails(interval, subject, previous_email_prompt, recipient, cc, bcc, presence_penalty_value, frequency_penalty_value)
                    message = "Email scheduling started."
            else:
                message = "Please enter a recipient email."

    login_status = "Logout" if defined_api_key and defined_email and defined_password else "Login"
    login_button_color = "#ff6b49" if login_status == "Logout" else "#4CAF50"          

    return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Generator</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                    color: #333;
                }}
                h1 {{
                    text-align: center;
                    padding: 20px;
                    color: #4CAF50;
                }}
                h2, h3 {{
                    color: #555;
                    margin-top: 20px;
                }}
                .container {{
                    display: flex;
                    flex-wrap: wrap;
                    max-width: 1400px;
                    margin: 20px auto;
                    gap: 40px;
                }}
                .half-section {{
                    flex: 1;
                    min-width: 500px;
                    padding: 20px;
                    background: #fff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }}
                .button-container {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 10px;
                }}
                label {{
                    font-weight: bold;
                }}
                textarea, input[type="email"], input[type="text"], input[type="password"], select {{
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-family: monospace;
                }}
                button {{
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-top: 10px;
                }}
                button:hover {{
                    background-color: #45a049;
                }}
                iframe {{
                    width: 100%;
                    height: 400px;
                    border: 1px solid #ddd;
                    background-color: #fff;
                    border-radius: 4px;
                    margin-top: 10px;
                }}
                img.preview-image {{
                    max-width: 100%;
                    height: auto;
                    margin-top: 10px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }}
                .message {{
                    color: green;
                    font-size: 1.1em;
                    margin-bottom: 20px;
                }}
                .popup-overlay {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.7);
                    display: none;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                }}
                .popup-content {{
                    background: #fff;
                    padding: 20px;
                    width: 90%;
                    max-width: 1000px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    position: relative;
                }}
                .close-popup {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: #f44336;
                    color: #fff;
                    border: none;
                    padding: 5px 10px;
                    cursor: pointer;
                    border-radius: 4px;
                }}
                .top-right-buttons {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    z-index: 10000;
                }}
            </style>
            <script>
                function openPopup(id) {{
                    document.getElementById(id).style.display = 'flex';
                }}

                function closePopup(id) {{
                    document.getElementById(id).style.display = 'none';
                }}
            </script>
        </head>
        <body>
            <div class="top-right-buttons">
                <button onclick="openPopup('loginPopup')" style="background-color: {login_button_color};">{login_status}</button>
                <button onclick="openPopup('configureModelPopup')">Configure Model</button>
            </div>
            
            <!-- Login Popup -->
            <div id="loginPopup" class="popup-overlay" onclick="closePopup('loginPopup')">
                <div class="popup-content" onclick="event.stopPropagation()">
                    <button class="close-popup" onclick="closePopup('loginPopup')">Close</button>
                    <h3>Login</h3>
                    <form method="POST">
                        <input type="password" name="api_key" placeholder="Enter OpenAI API Key">
                        <input type="text" name="email" placeholder="Enter Email">
                        <input type="password" name="password" placeholder="Enter Password">
                        <button type="submit" name="action" value="Login">Login</button>
                        <button type="submit" name="action" value="Logout" style="background-color: #ff6b49;">Logout</button>
                    </form>
                </div>
            </div>

            <!-- Configure Model Popup -->
            <div id="configureModelPopup" class="popup-overlay" onclick="closePopup('configureModelPopup')">
                <div class="popup-content" onclick="event.stopPropagation()">
                    <button class="close-popup" onclick="closePopup('configureModelPopup')">Close</button>
                    <h3>Configure Model</h3>
                    <form method="POST">
                        <label>Generate HTML Template Model:</label>
                        <select name="generate_html_template_model">
                            <option value="gpt-3.5-turbo" {'selected' if generate_html_template_model == 'gpt-3.5-turbo' else ''}>GPT-3.5 Turbo</option>
                            <option value="gpt-4" {'selected' if generate_html_template_model == 'gpt-4' else ''}>GPT-4</option>
                        </select>
                        <label>Generate Email Content Model:</label>
                        <select name="generate_email_content_model">
                            <option value="gpt-3.5-turbo" {'selected' if generate_email_content_model == 'gpt-3.5-turbo' else ''}>GPT-3.5 Turbo</option>
                            <option value="gpt-4" {'selected' if generate_email_content_model == 'gpt-4' else ''}>GPT-4</option>
                        </select>
                        <label>Merge HTML and Content Model:</label>
                        <select name="merge_html_and_content_via_llm_model">
                            <option value="gpt-3.5-turbo" {'selected' if merge_html_and_content_via_llm_model == 'gpt-3.5-turbo' else ''}>GPT-3.5 Turbo</option>
                            <option value="gpt-4" {'selected' if merge_html_and_content_via_llm_model == 'gpt-4' else ''}>GPT-4</option>
                        </select>
                        <label>Generate Summary Keyword Model:</label>
                        <select name="generate_summary_keyword_model">
                            <option value="gpt-3.5-turbo" {'selected' if generate_summary_keyword_model == 'gpt-3.5-turbo' else ''}>GPT-3.5 Turbo</option>
                            <option value="gpt-4" {'selected' if generate_summary_keyword_model == 'gpt-4' else ''}>GPT-4</option>
                        </select>
                        <button type="submit" name="action" value="Configure Model">Save Configuration</button>
                    </form>
                </div>
            </div>

            <!-- LOGO -->
            <div style="text-align: center;">
    <img src="https://i.imgur.com/yJ8xPm6.png" alt="Mailmancer Logo" style="max-width: 400px; height: auto;">
</div>

            <!-- Part 1: Step 1 - Generate HTML Template and Preview -->
            <div class="container">
                <div class="half-section">
                    <form method="POST">
                        <h2>Step 1: Generate HTML Template</h2>
                        <textarea name="html_prompt" placeholder="Enter your HTML prompt here..." style="height: 400px;">{html.escape(previous_html_prompt)}</textarea>
                        <button type="submit" name="action" value="Generate HTML Template">Generate HTML Template</button>
                    </form>
                    <div id="addTemplatePopup" class="popup-overlay" onclick="closePopup('addTemplatePopup')">
                        <div class="popup-content" onclick="event.stopPropagation()">
                            <button class="close-popup" onclick="closePopup('addTemplatePopup')">Close</button>
                            <h3>Add Custom Template</h3>
                            <form method="POST">
                                <textarea name="custom_template" placeholder="Enter your custom template here..." style="height: 200px;"></textarea>
                                <button type="submit" name="action" value="Add Template">Save</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="half-section">
                    <h3>HTML Template Preview
                        <button type="button" style="float: right; margin-top: -5px;" onclick="openPopup('htmlTemplatePopup')">Expand</button>
                    </h3>
                    <div class="button-container" style="float: left; margin-top: -15px;">
                        <form method="POST">
                            <button type="submit" name="action" value="Template 1">Template 1</button>
                            <button type="submit" name="action" value="Template 2">Template 2</button>
                            <button type="submit" name="action" value="Template 3">Template 3</button>
                            <button type="button" onclick="openPopup('addTemplatePopup')">Add Template</button>
                        </form>
                    </div>
                    <iframe srcdoc="{html.escape(rendered_html_preview)}" sandbox="allow-same-origin allow-scripts" style="height: 400px;"></iframe>
                </div>
            </div>

            <!-- HTML Template Popup -->
            <div id="htmlTemplatePopup" class="popup-overlay" onclick="closePopup('htmlTemplatePopup')">
                <div class="popup-content" onclick="event.stopPropagation()">
                    <button class="close-popup" onclick="closePopup('htmlTemplatePopup')">Close</button>
                    <h3>HTML Template Full Page Preview</h3>
                    <iframe srcdoc="{html.escape(rendered_html_preview)}" sandbox="allow-same-origin allow-scripts" style="width: 100%; height: 80vh;"></iframe>
                </div>
            </div>

            <!-- Part 2: Step 2 - Generate Final Email Content and Editable Preview -->
            <div class="container">
                <div class="half-section">
                    <form method="POST">
                        <h2>Step 2: Generate Final Email Content</h2>
                        <textarea name="email_prompt" placeholder="Enter your email prompt here..." style="height: 300px;">{html.escape(previous_email_prompt)}</textarea>
                        <button type="submit" name="action" value="Generate Final Email Content">Generate Final Email Content</button>
                    </form>
                </div>
                <div class="half-section">
                    <h3>Editable Content Preview</h3>
                    <form method="POST">
                        <textarea name="current_email_content" placeholder="Edit your email content here..." style="height: 300px;">{html.escape(final_email_content)}</textarea>
                        <button type="submit" name="action" value="Save Email Content Changes">Save Email Content Changes</button>
                    </form>
                </div>
            </div>

            <!-- Part 3: Generate Email Image and Preview -->
            <div class="container">
                <div class="half-section">
                    <form method="POST">
                        <h2>Step 3: Generate Email Image</h2>
                        <label><input type="radio" name="use_custom_prompt" value="no" checked> Use email content as image prompt</label><br>
                        <label><input type="radio" name="use_custom_prompt" value="yes"> Write custom prompt for image</label><br>
                        <input type="text" name="custom_image_prompt" placeholder="Enter your custom image prompt here..." value="{html.escape(custom_image_prompt)}">
                        <button type="submit" name="action" value="Generate Email Image">Generate Email Image</button>
                    </form>
                </div>
                <div class="half-section">
                    <h3>Generated Image Preview</h3>
                    <form method="POST">
                        <input type="text" name="image_url" value="{html.escape(image_url)}" placeholder="Edit image URL here...">
                        <button type="submit" name="action" value="Save Image URL">Save Image URL</button>
                    </form>
                    {f'<img src="{image_url}" alt="Generated Email Image" class="preview-image">' if image_url else ''}
                </div>
            </div>

            <!-- Part 4: Generate Background Image and Preview (Optional) -->
<div class="container">
    <div class="half-section">
        <form method="POST">
            <h2>Step 4: Generate Background Image (Optional)</h2>
            <label><input type="radio" name="use_custom_background_prompt" value="no" checked> Use email content as background prompt</label><br>
            <label><input type="radio" name="use_custom_background_prompt" value="yes"> Write custom prompt for background</label><br>
            <input type="text" name="custom_background_prompt" placeholder="Enter your custom background prompt here..." value="{html.escape(custom_background_prompt)}">

            <button type="submit" name="action" value="Generate Background Image">Generate Background Image</button>
        </form>
    </div>
    <div class="half-section">
        <h3>Generated Background Image Preview</h3>
        <form method="POST">
            <input type="text" name="background_image_url" value="{html.escape(background_image_url)}" placeholder="Edit background image URL here...">
            <button type="submit" name="action" value="Save Background Image URL">Save Background Image URL</button>
        </form>
        {f'<img src="{background_image_url}" alt="Generated Background Image" class="preview-image">' if background_image_url else ''}
    </div>
</div>

            <!-- Part 5: Generate Combined Email Preview -->
            <div class="container">
                <div class="half-section">
                    <form method="POST">
                        <h2>Step 5: Generate Combined Email Preview</h2>

                        <h3>Apply Background Image To:</h3>
                        <label><input type="radio" name="background_usage" value="body" checked> Body Background</label><br>
                        <label><input type="radio" name="background_usage" value="container"> Container Background</label><br>
                        
                        <button type="submit" name="action" value="Generate Combined Email Preview">Generate Combined Email Preview</button>
                    </form>
                    <form method="POST">
                        <h3>Editable Combined HTML Output</h3>
                        <textarea name="combined_html_content" placeholder="Edit combined HTML content here..." style="height: 300px;">{html.escape(final_combined_email)}</textarea>
                        <button type="submit" name="action" value="Save Combined HTML Changes">Save Combined HTML Changes</button>
                    </form>
                </div>
                <div class="half-section">
                    <h3>Combined Email Preview</h3>
                    <button type="button" style="float: right; margin-top: -50px;" onclick="openPopup('combinedEmailPopup')">Expand</button>
                    <iframe srcdoc="{html.escape(final_combined_email)}" sandbox="allow-same-origin allow-scripts"></iframe>
                </div>
            </div>

            <!-- Combined Email Popup -->
            <div id="combinedEmailPopup" class="popup-overlay" onclick="closePopup('combinedEmailPopup')">
                <div class="popup-content" onclick="event.stopPropagation()">
                    <button class="close-popup" onclick="closePopup('combinedEmailPopup')">Close</button>
                    <h3>Combined Email Full Page Preview</h3>
                    <iframe srcdoc="{html.escape(final_combined_email)}" sandbox="allow-same-origin allow-scripts" style="width: 100%; height: 80vh;"></iframe>
                </div>
            </div>
       <!-- Part 6: Step 6 - Send Email -->
<div class="container">
    <div class="half-section">
        <form method="POST">
            <h2>Step 6: Send Email</h2>
            <label for="recipient">Recipient Email:</label>
            <input type="email" id="recipient" name="recipient" placeholder="Enter recipient email">
            <label for="cc">CC:</label>
            <input type="text" id="cc" name="cc" placeholder="Enter CC emails (comma separated)">
            <label for="bcc">BCC:</label>
            <input type="text" id="bcc" name="bcc" placeholder="Enter BCC emails (comma separated)">
            <label for="email_subject">Subject:</label>
            <input type="text" id="email_subject" name="email_subject" value="{html.escape(extract_subject_or_header(final_email_content) or 'Generated Email')}">
            <h3>Send Settings</h3>
            
            <label><input type="radio" name="send_option" value="One-Time Only" checked> One-Time Only</label><br>
            <label><input type="radio" name="send_option" value="Send at Regular Intervals"> Send at Regular Intervals</label><br>
            <input type="text" name="interval" placeholder="Enter interval in minutes (default 60)" style="display:none;" id="interval_input">
            <h3>Content Settings</h3>
            <label><input type="checkbox" name="use_keyword_summary" value="yes"> Use keyword summary feature to avoid content repetition</label><br>

            
<br>
<button type="submit" name="action" value="Send Email">Send Email</button>
        </form>
    </div>
    <div class="half-section">
        <h3>Combined Email Preview</h3>
        <iframe srcdoc="{html.escape(final_combined_email or '')}" sandbox="allow-same-origin allow-scripts"></iframe>
    </div>
</div>

<script>
    document.querySelectorAll('input[name="send_option"]').forEach(function(option) {{
        option.addEventListener('change', function() {{
            const intervalInput = document.getElementById('interval_input');
            if (this.value === 'Send at Regular Intervals') {{
                intervalInput.style.display = 'block';
            }} else {{
                intervalInput.style.display = 'none';
            }}
        }});
    }});
    document.querySelector('input[name="use_presence_penalty"]').addEventListener('change', function() {{
        const presencePenaltyInput = document.getElementById('presence_penalty_input');
        if (this.checked) {{
            presencePenaltyInput.style.display = 'block';
        }} else {{
            presencePenaltyInput.style.display = 'none';
        }}
    }});
    document.querySelector('input[name="use_frequency_penalty"]').addEventListener('change', function() {{
        const frequencyPenaltyInput = document.getElementById('frequency_penalty_input');
        if (this.checked) {{
            frequencyPenaltyInput.style.display = 'block';
        }} else {{
            frequencyPenaltyInput.style.display = 'none';
        }}
    }});
</script>
</body>
</html>
    """)

if __name__ == "__main__":
    app.run(debug=True)

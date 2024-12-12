# Sample HTML templates
TEMPLATES = {
    "template_1": """
<!DOCTYPE html>
<html>
<head>
    <title>Lorem Ipsum Subject</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            text-align: center; /* Body alignment is controlled independently */
        }
        .email-container {
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .email-header {
            text-align: center;
            border-bottom: 1px solid #dddddd;
            padding-bottom: 10px;
        }
        .email-header h1 {
            color: #333333;
            font-size: 24px;
            margin: 0;
        }
        .email-body {
            padding: 20px;
            color: #555555;
            font-size: 16px;
        }
        .email-body img {
            max-width: 100%;
            height: auto;
            margin-bottom: 20px;
            border-radius: 8px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .email-body p {
            margin: 0 0 10px;
            text-align: left;
        }
        .discover-more-button-container {
            text-align: center; /* Button alignment is controlled independently */
            margin-top: 20px;
        }
        .discover-more-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #808080; /* Grey background color */
            color: #ffffff;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
        }
        .email-footer {
            text-align: center;
            margin-top: 20px;
            color: #888888;
            font-size: 12px;
        }
        .email-footer a {
            color: #555555;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>Lorem Ipsum Header</h1>
        </div>
        <div class="email-body">
            <img src="https://via.placeholder.com/600x200" alt="Filler Image">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque non dolor vitae erat mollis gravida. Integer nec consequat risus. Vestibulum non orci at metus malesuada tempus.</p>
            <p>Suspendisse potenti. Nullam vehicula, augue id fringilla luctus, sem orci accumsan lacus, eget ultricies nisi ligula a felis. Donec sodales dapibus diam, nec tincidunt lectus laoreet et.</p>
            <div class="discover-more-button-container">
                <a href="https://example.com/discover" class="discover-more-button">Discover More</a>
            </div>
        </div>
        <div class="email-footer">
            <p>Thank you for being with us.</p>
            <p><a href="https://example.com/unsubscribe">Unsubscribe</a> if you no longer wish to receive these emails.</p>
        </div>
    </div>
</body>
</html>
""",
    "template_2": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lorem Ipsum Announcement</title>
    <style>
        body {
            font-family: Georgia, serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            text-align: left; /* Body alignment is now separate */
        }
        .container {
            max-width: 800px;
            margin: 60px auto;
            padding: 20px;
            background-color: #ffffff;
            border: 2px solid #999;
            border-radius: 16px;
        }
        .header-section {
            padding: 30px;
            border-bottom: 2px dotted #aaa;
            text-align: center;
        }
        .header-section h1 {
            font-size: 32px;
            margin: 0;
            line-height: 1.2;
        }
        .intro-section {
            padding: 25px;
            font-style: italic;
        }
        .intro-section p {
            margin: 0;
            font-size: 18px;
        }
        .image-section {
            text-align: center;
            padding: 20px 0;
        }
        .image-section img {
            max-width: 100%;
            height: auto;
        }
        .body-section {
            padding: 40px;
        }
        .body-section p {
            margin-bottom: 25px;
            font-size: 16px;
            line-height: 1.8;
        }
        .button-container {
            text-align: center; /* Button alignment is controlled independently */
            padding: 30px;
        }
        .cta-link {
            font-size: 18px;
            padding: 12px 20px;
            border: 1px dashed #333;
            background-color: #808080; /* Grey button background */
            color: #ffffff;
            text-decoration: none;
            font-weight: bold;
            border-radius: 6px;
        }
        .cta-link:hover {
            background-color: #6d6d6d;
        }
        .footer-section {
            padding: 20px;
            border-top: 2px dotted #aaa;
            text-align: right;
            font-size: 14px;
            color: #555;
        }
        .unsubscribe-link {
            display: block;
            margin-top: 10px;
            font-size: 14px;
            text-decoration: none;
            color: #888;
        }
        .unsubscribe-link:hover {
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>Lorem Ipsum Dolor Sit Amet</h1>
        </div>
        <div class="intro-section">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam et urna at quam ullamcorper laoreet.</p>
        </div>
        <div class="image-section">
            <img src="https://via.placeholder.com/600x200" alt="Placeholder Image">
        </div>
        <div class="body-section">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ultricies turpis, in luctus magna. Praesent tincidunt lacus justo, non commodo ligula auctor vel. Donec tempor dui eu arcu elementum, id congue mauris bibendum. Aliquam erat volutpat. Curabitur nec lacus sapien. Duis scelerisque a libero in faucibus. Vivamus id ligula id libero tempus aliquam vel non nisl. Etiam sit amet turpis quis odio accumsan vestibulum at ac enim.</p>
            <p>Aliquam vitae sapien a felis facilisis gravida a at erat. Ut elementum mi eget orci fringilla, sit amet bibendum nisi scelerisque. Sed posuere, lorem sit amet accumsan accumsan, magna velit scelerisque leo, ac condimentum lacus metus ac justo. Nulla facilisi.</p>
        </div>
        <div class="button-container">
            <a href="#" class="cta-link">Learn More</a>
        </div>
        <div class="footer-section">
            <p>&copy; 2024 Lorem Ipsum Corporation. All rights reserved.</p>
            <a href="#" class="unsubscribe-link">Unsubscribe</a>
        </div>
    </div>
</body>
</html>
""",
    "template_3": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lorem Ipsum Special Update</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            background-color: #fafafa;
            text-align: left; /* Body alignment set independently */
        }
        .container {
            max-width: 800px;
            margin: 60px auto;
            padding: 0;
            background-color: #ffffff;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
        }
        .header-section {
            background: linear-gradient(135deg, #f0f0f0, #d3d3d3);
            padding: 40px;
            text-align: center;
        }
        .header-section h1 {
            font-size: 32px;
            margin: 0;
            line-height: 1.5;
            color: #444;
        }
        .intro-section {
            padding: 30px;
            background-color: #f9f9f9;
            border-left: 10px solid #444;
            font-style: italic;
        }
        .intro-section p {
            margin: 0;
            font-size: 18px;
            line-height: 1.7;
            color: #666;
        }
        .image-section {
            text-align: center;
            padding: 20px;
            background-color: #ffffff;
        }
        .image-section img {
            max-width: 100%;
            border-radius: 12px;
        }
        .body-section {
            padding: 40px;
            text-align: justify;
            background-color: #f5f5f5;
        }
        .body-section p {
            margin-bottom: 20px;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
        }
        .quote-section {
            padding: 30px;
            background-color: #e0e0e0;
            border-radius: 12px;
            text-align: center;
            margin: 30px;
        }
        .quote-section p {
            font-size: 20px;
            font-weight: bold;
            color: #555;
            margin: 0;
        }
        .button-container {
            padding: 30px;
            text-align: center; /* Button alignment controlled independently */
        }
        .cta-link {
            font-size: 18px;
            padding: 14px 28px;
            border: 2px solid #333;
            background-color: #808080; /* Grey button background */
            color: #ffffff;
            text-decoration: none;
            font-weight: bold;
            border-radius: 25px;
            transition: background-color 0.3s, color 0.3s;
        }
        .cta-link:hover {
            background-color: #6d6d6d;
            color: #ffffff;
        }
        .footer-section {
            padding: 20px;
            background-color: #333;
            color: #fff;
            text-align: center;
            font-size: 14px;
        }
        .unsubscribe-link {
            display: block;
            margin-top: 10px;
            font-size: 14px;
            text-decoration: none;
            color: #bbb;
        }
        .unsubscribe-link:hover {
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>Lorem Ipsum Dolor Sit Amet</h1>
        </div>
        <div class="intro-section">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Donec vehicula odio vel nibh vehicula pretium.</p>
        </div>
        <div class="image-section">
            <img src="https://via.placeholder.com/600x200" alt="Placeholder Image">
        </div>
        <div class="body-section">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sed feugiat nulla. Nulla facilisi. Cras nec diam sit amet eros gravida cursus a ac justo. Ut nec diam id nunc dignissim consectetur sed quis ex. Vivamus ac sapien eget metus malesuada ultricies.</p>
            <p>Praesent auctor ligula nec quam tempus, a dapibus magna laoreet. Phasellus suscipit arcu ac neque malesuada, sed ultrices odio vestibulum. Integer iaculis augue velit, et pretium ligula finibus non. Suspendisse vestibulum urna non massa fermentum, at ultrices risus interdum.</p>
        </div>
        <div class="quote-section">
            <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit."</p>
        </div>
        <div class="button-container">
            <a href="#" class="cta-link">Discover More</a>
        </div>
        <div class="footer-section">
            <p>&copy; 2024 Lorem Ipsum Corporation. All rights reserved.</p>
            <a href="#" class="unsubscribe-link">Unsubscribe</a>
        </div>
    </div>
</body>
</html>
""",
}

previous_html_prompt = """
Example Prompt:

Body:
- Change the background color to pastel blue (`#bfe7ff`).
- Set the font family to 'Arial'.
- Adjust the line height to 1.8.

Email Container:
- Change the background color to pastel yellow ('#ffffcc').
- Modify the container width to 600px.
- Modify the border radius to 12px.

Header:
- Change the header text color to pastel pink (`#f8adcc`).
- Set a header background color to a pastel white (`#faf8f6`).
- Increase the font size of the header text to 32px.

Email Body:
- Update the paragraph text color to dark gray (`#555555`).
- Set the font size to 18px.
- Add 10px spacing between paragraphs.

Body Button Customizations:
- 2 Buttons in total, in the mail body:
- Name Button 1 to Visit our Website, and link it to 'https://example.com/'.
- Name Button 2 to Instagram, and link it to 'https://example.com/'.
- Make buttons pastel green ('#80ef80').
- Place buttons side to side.

Placeholder Image:
- Allign it to the middle of the body.

Footer:
- Change the footer text color to gray (`#888888`).
- Make the footer Unsubscribe button bold and update its color to blue (`#0000FF`).
- Change Unsubscribe button link to 'https://example.com/'.
- Add more spacing between the footer text and links.
"""

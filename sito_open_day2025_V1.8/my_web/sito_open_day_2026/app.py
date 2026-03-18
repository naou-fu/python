from flask import Flask, render_template, send_from_directory
import os
from jinja2 import FileSystemLoader

app = Flask(
    __name__,
    static_folder=None
)

# Set custom template folder
app.jinja_loader = FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'HTML_V1.0')
)

# Serve HTML
@app.route('/')
def home():
    return render_template('First_Page_1.html')

@app.route('/Second_Page_2')
def second_page_2():
    return render_template('Second_Page_2.html')

@app.route('/Third_Page_3')
def third_page_3():
    return render_template('Third_Page_3.html')

@app.route('/Fourth_Page_4')
def fourth_page_4():
    return render_template('Fourth_Page_4.html')

@app.route('/Fifth_Page_5')
def fifth_page_5():
    return render_template('Fifth_Page_5.html')

@app.route('/Sixth_Page_6')
def sixth_page_6():
    return render_template('Sixth_Page_6.html')

@app.route('/Seventh_Page_7')
def seventh_page_7():
    return render_template('Seventh_Page_7.html')

# Serve CSS
@app.route('/CSS_V1.0/<path:filename>')
def css(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'CSS_V1.0'), filename)

# Serve images
@app.route('/PNG_JPEG/<path:filename>')
def images(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'PNG_JPEG'), filename)

# Serve videos and gifs
@app.route('/VIDEOS_GIF/<path:filename>')
def videos_gif(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'VIDEOS_GIF'), filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
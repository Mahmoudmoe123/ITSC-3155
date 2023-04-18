from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def dashboard():
    dorms = [
        {
            'name': 'Martin Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623139572.069_500_348.jpg',
            'rating': '4.2'
        },
        {
            'name': 'Holshouser Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623097272.604_500_348.jpg',
            'rating': '4.0'
        },
        {
            'name': 'Scott Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623243475.225_500_348.jpg',
            'rating': '3.9'
        }
    ]
    return render_template('dashboard.html', dorms=dorms)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')


if __name__ == '__main__':
    app.run(debug=True)
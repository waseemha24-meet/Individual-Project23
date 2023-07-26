from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyAk36ZkUUs9EG05ngO4l_MNml8AGrhJX4E",
  "authDomain": "cs-project-31a57.firebaseapp.com",
  "projectId": "cs-project-31a57",
  "storageBucket": "cs-project-31a57.appspot.com",
  "messagingSenderId": "443682324597",
  "appId": "1:443682324597:web:c574e340b8e9aa75b8b83c",
  "measurementId": "G-KLPF3SR0GJ",
  "databaseURL": "https://cs-project-31a57-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def get_started():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authetication faild"
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user=auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template('login.html')
@app.route('/information')
def buttons():
    return render_template('information.html')

@app.route('/info')
def index():
    return render_template('info.html')


@app.route('/result', methods=['POST'])
def result():
    user_pet = request.form.get('pet')
    if 'display_data' in request.form:
        data = get_data_for_pet(user_pet)
        return render_template('informaton.html', data=data)
    elif 'say_hi' in request.form:
        data = train_pet(user_pet)
        return render_template('informaton.html', data=data)
    return "Invalid form submission."

def get_data_for_pet(pet_choice):
    pet_data = {
        'dog': {
            'name': 'Dog',
            'description': 'A dog is a domestic mammal of the family Canidae and the order Carnivora. Its scientific name is Canis lupus familiaris. Dogs are a subspecies of the gray wolf, and they are also related to foxes and jackals. Dogs are one of the two most ubiquitous and most popular domestic animals in the world. (Cats are the other.)',
            'one' : 'Barking is a way for dogs to communicate with other dogs and with humans. Fierce barking or growling often signals that dogs are being territorial, feel threatened, or simply want to be left alone. However, dogs also bark when they are bored and want attention from other dogs or from humans.' ,
            'two': 'A dog may sniff other dogs’ rear ends to gather chemical information that helps the sniffer identify them as individuals. Gland-lined sacs, housed internally on either side of a dog’s anus, produce a scent that contributes to each dog’s unique odour profile. That profile may also indicate genetic makeup, reproductive status, diet, and emotional state.' , 
            'photo': 'https://cdn.britannica.com/42/8142-004-4CD3860D/Boxer.jpg?w=400&h=300&c=crop',
            'video': 'https://youtu.be/1BUWbewRPGI'
        },
        'cat': {
            'name': 'Cat',
            'description': 'Cats are known for their unusual behavior and peculiarities. While many cat lovers think they know everything about their feline friends, there are still some weird and surprising facts about cats that many people don’t know. Here are the top 10 weirdest facts about cats.',
            'one' : 'While this characteristic is not scientifically known as having a “sixth sense,” cats’ senses are more sensitive which gives them an amazing ability to sense vibrations and frequencies that humans cannot perceive. For example, they can detect subtle changes in the air, which allows them to sense approaching danger or even supposedly detect earthquakes before humans can.',
            'two' : 'Cats have a layer of cells called the tapetum lucidum that reflects light back through the retina, allowing them to see in low-light conditions – the reason their eyes seem to glow in the dark.',
            'photo': 'https://vid.alarabiya.net/images/2021/08/18/72b65744-bf80-4406-a2e5-48f286d18699/72b65744-bf80-4406-a2e5-48f286d18699_16x9_1200x676.jpg?width=1120&format=jpg',
            'video': 'https://youtu.be/pX3V9hoX1eM'
        }
    }
    return pet_data.get(pet_choice, None)


def train_pet(pet_choice):
    pet_data = {
        'dog': {
            'name': 'Dog',
            'description': "The most popular way to teach sit is with lure and reward training using a handful of delicious treats. A clicker can also help mark the exact moment your dog sits. To guarantee success, train when your dog is relaxed in an environment without distractions. The following steps will lure a sit:\n 1. With your dog standing, hold a treat to their nose.\n Slowly lift the treat over their head towards their rear. As your dog lifts their head to follow the treat with their nose, their back end should drop to the ground.\n 2. As soon as your dog is in a sitting position, click your clicker and/or praise them and offer the treat as a reward. \n 3.  To get your dog standing again, either walk away and call them over or toss another treat a few feet away. Then repeat steps 1 to 3. \n Once your dog will reliably follow the treat into a sitting position, it’s time to fade the lure. Now use an empty hand to lure the dog and reward the sit with a treat from your other hand. The movement of your empty hand will become your hand signal. \n 4. When your dog reliably sits for your empty hand, you can add your verbal cue “Sit” right before you give the hand signal. In time, your dog should respond to the verbal cue alone.",
            'one' : "" ,
            'two': "" , 
            'photo': "",
            'video': ""
        },
        'cat': {
            'name': 'Cat',
            'description': '',
            'one' : '',
            'two' : '',
            'photo': '',
            'video': ''
        }
    }
    return pet_data.get(pet_choice, None)

@app.route('/home' , methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        caption = request.form['caption']
        link = request.form['image']
        user_post = {"caption" : caption , "link" : link}
        db.child("Posts").child(login_session['user']['localId']).set(user_post)
        return render_template('home.html' , post = user_post)
    else:
        user_post = db.child("Posts").child(login_session['user']['localId']).get().val()
        return render_template('home.html', post = user_post)


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
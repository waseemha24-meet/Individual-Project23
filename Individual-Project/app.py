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
        },
        'cat': {
            'name': 'Cat',
            'description': 'Cats are known for their unusual behavior and peculiarities. While many cat lovers think they know everything about their feline friends, there are still some weird and surprising facts about cats that many people don’t know. Here are the top 10 weirdest facts about cats.',
            'one' : 'While this characteristic is not scientifically known as having a “sixth sense,” cats’ senses are more sensitive which gives them an amazing ability to sense vibrations and frequencies that humans cannot perceive. For example, they can detect subtle changes in the air, which allows them to sense approaching danger or even supposedly detect earthquakes before humans can.',
            'two' : 'Cats have a layer of cells called the tapetum lucidum that reflects light back through the retina, allowing them to see in low-light conditions – the reason their eyes seem to glow in the dark.',
            'photo': 'https://vid.alarabiya.net/images/2021/08/18/72b65744-bf80-4406-a2e5-48f286d18699/72b65744-bf80-4406-a2e5-48f286d18699_16x9_1200x676.jpg?width=1120&format=jpg',
        }
    }
    return pet_data.get(pet_choice, None)


def train_pet(pet_choice):
    pet_data = {
        'dog': {
            'name': 'Dog',
            'description': "make you dog sitting: \n The most popular way to teach sit is with lure and reward training using a handful of delicious treats. A clicker can also help mark the exact moment your dog sits. To guarantee success, train when your dog is relaxed in an environment without distractions. The following steps will lure a sit:\n 1. With your dog standing, hold a treat to their nose.\n Slowly lift the treat over their head towards their rear. As your dog lifts their head to follow the treat with their nose, their back end should drop to the ground.\n 2. As soon as your dog is in a sitting position, click your clicker and/or praise them and offer the treat as a reward. \n 3.  To get your dog standing again, either walk away and call them over or toss another treat a few feet away. Then repeat steps 1 to 3. \n Once your dog will reliably follow the treat into a sitting position, it’s time to fade the lure. Now use an empty hand to lure the dog and reward the sit with a treat from your other hand. The movement of your empty hand will become your hand signal. \n 4. When your dog reliably sits for your empty hand, you can add your verbal cue “Sit” right before you give the hand signal. In time, your dog should respond to the verbal cue alone.",
            'one' : "With your dog in a sitting position and a treat in your hand, move your hand from your dog's nose towards their chest, then straight down towards the floor. \n 1.Your dog should follow the treat into a lying down position. Praise and reward them with the treat immediately.\n 2.Practice this a number of times in short but regular sessions.\n 3.When your dog is easily following the treat into a down position, you can start to say the word 'down' just as your dog is getting into the down position.\n 3.Practice this a number of times in short but regular sessions.\n 4.While your dog is lying down, give him treats - this will increase the time he spends lying down." ,
            'two': "Pick a bathroom spot outside, and always take your puppy (on a leash) to that spot. While your puppy is relieving themselves, use a specific word or phrase that you can eventually use before they go to remind them what to do. Take them out for a longer walk or some playtime only after they have eliminated." , 
            'photo': "data:image/jpeg;base64,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",
        },
        'cat': {
            'name': 'Cat',
            'description': 'To train your cat to lie down, choose a quiet and comfortable space where your feline friend feels relaxed and safe, ensuring minimal distractions to maintain their focus. Utilize treats or a favorite toy as positive reinforcement to encourage the desired behavior. Instead of trying to lure your cat into a lying down position, focus on capturing the behavior when your cat naturally lies down, often feeling comfortable and at ease. Timing is crucial; use a clicker or a specific word like "Down" in a gentle and calm voice immediately when your cat lies down to associate the command with the action. Reward and repeat this process whenever you catch your cat lying down naturally.\nAs your cat starts associating the command with the behavior, introduce the verbal cue "Lie down" or any short phrase before your cat lies down to strengthen the connection between the command and the action. Keep training sessions brief and positive, considering your cats short attention span. Aim for a few minutes of training each day. Patience and understanding are paramount in cat training, as some cats may take longer to learn certain behaviors, and punishing your cat during training can be counterproductive.\nConsistency plays a vital role; use the same command, maintain patience, and reinforce positive behavior with rewards. Always end training sessions on a positive note, praising your cat and offering a treat for their effort, even if they havent fully grasped the command yet. Building a strong bond with your feline companion is essential, so focus on reinforcing other positive behaviors and understanding your cats unique personality throughout the training process.',
            'one' : 'To train your cat to use the litter box or a specific bathroom spot, choose an appropriate litter box or designated area, observe your cats natural habits, and provide positive reinforcement like praise and treats when they use the desired location. Be consistent with the spot and timing, keeping the litter box clean, and avoiding scolding if accidents occur. Monitor your cats progress, address accidents promptly, and be patient throughout the training process. Additionally, pay attention to any changes in your cats bathroom habits and consult a veterinarian if needed. With time, consistency, and understanding, you can successfully train your cat to use the designated bathroom area.',
            'two' : '',
            'photo': 'https://www.pumpkin.care/wp-content/uploads/2022/01/how-to-train-your-cat.jpg',
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
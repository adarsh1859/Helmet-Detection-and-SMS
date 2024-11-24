



from flask import Flask, render_template, request, redirect,jsonify
import cv2
import time
import os
import easyocr
from my_functions import *
from PIL import Image
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# @app.route('/')
# def index():
#     return render_template('index.html') #earlier code
#     # return render_template('login.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/')
def login():
    # return render_template('index.html') #earlier code
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/fetch')
def fetch():
    return render_template('fetch.html')

@app.route('/image')
def image():
    return render_template('image.html')



@app.route('/static/riders_pictures/')
def get_number_plates():
    # Get the list of image filenames from a directory
    image_files = os.listdir('static/riders_pictures/')
    return jsonify(image_files)

@app.route('/static/number_plates/')
def get_riders_pictures():
    # Get the list of image filenames from a directory
    image_files = os.listdir('static/number_plates/')
    return jsonify(image_files)


@app.route('/process', methods=['POST'])
def process_video():
    source = request.files['videoSource']
    save_video = request.form.get('saveVideo') == 'true'
    show_video = True
    # show_video =request.form.get('saveVideo') == 'true'
    save_img = request.form.get('saveImg') == 'true'  # Fixed the boolean conversion

    # Define frame size based on your requirement
    frame_size = (800, 480)

    # Initialize video writer if saving video
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)

    # Create output folder if it doesn't exist
    output_folder = 'output_texts'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert source to string
    source_path = source.filename if hasattr(source, 'filename') else source

    cap = cv2.VideoCapture(source_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, frame_size)  # resizing image
            original_frame = frame.copy()
            frame, results = object_detection(frame) 

            rider_list = []
            head_list = []
            number_list = []

            for result in results:
                x1, y1, x2, y2, cnf, clas = result
                if clas == 0:
                    rider_list.append(result)
                elif clas == 1:
                    head_list.append(result)
                elif clas == 2:
                    number_list.append(result)

            for rdr in rider_list:
                time_stamp = str(time.time())
                x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                for hd in head_list:
                    x1h, y1h, x2h, y2h, cnfh, clash = hd
                    if inside_box([x1r, y1r, x2r, y2r], [x1h, y1h, x2h, y2h]):
                        try:
                            head_img = original_frame[y1h:y2h, x1h:x2h]
                            helmet_present = img_classify(head_img)
                        except:
                            helmet_present = [None, 0]

                        if helmet_present[0] == True: # if helmet present
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                        elif helmet_present[0] == None: # Poor prediction
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                        elif helmet_present[0] == False: # if helmet absent 
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                            try:
                                cv2.imwrite(f'static/riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                            except:
                                print('could not save rider')

                            for num in number_list:
                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                if inside_box([x1r, y1r, x2r, y2r], [x1_num, y1_num, x2_num, y2_num]):
                                    try:
                                        num_img = original_frame[y1_num:y2_num, x1_num:x2_num]
                                        cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                                    except:
                                        print('could not save number plate')

            if save_video: # save video
                out.write(frame)
            if save_img: #save img
                cv2.imwrite('saved_frame.jpg', frame)
            if show_video: # show video
                frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
                cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    if save_video:
        out.release()
    cv2.destroyAllWindows()
    # return 'executed'
    return redirect('/fetch_images')


@app.route('/fetch_images', methods=['GET'])
def fetch_images():
    input_folder = 'number_plates'
    output_folder = 'output_texts'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_text_from_images(input_folder, output_folder)

    return 'Images fetched and text extracted successfully!'


def extract_text_from_images(input_folder, output_folder):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each image file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)

            # Read image using PIL
            image = Image.open(image_path)

            # Extract text using EasyOCR
            result = reader.readtext(image)

            # Write extracted text to a text file in the output folder
            output_text_filename = os.path.splitext(filename)[0] + ".txt"
            output_text_path = os.path.join(output_folder, output_text_filename)

            with open(output_text_path, "w") as text_file:
                for detection in result:
                    text_file.write(detection[1] + "\n")

            print(f"Text extracted from {filename} and saved to {output_text_filename}")



# Predefined path to the text folder (change this to your actual path)

txt_folder = 'output_texts'



@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/render')
def render():
    return render_template('render.html')

@app.route('/image1')
def image1():
    return render_template('image1.html')

     
# @app.route('/search')
# def search():
#     xml_file = 'rider-data-500.xml'  # Change this to your actual XML file path
#     matches = []

#     # Check if text folder exists
#     if not os.path.exists(txt_folder):
#         return render_template('result.html', message="Text folder not found!")

#     # Read XML file
#     try:
#         tree = ET.parse(xml_file)
#         root = tree.getroot()
#     except FileNotFoundError:
#         return render_template('result.html', message="XML file not found!")

#     # Loop through files in the folder
#     for filename in os.listdir(txt_folder):
#         if filename.endswith('.txt'):
#             txt_path = os.path.join(txt_folder, filename)
#             try:
#                 with open(txt_path, 'r') as f:
#                     text_to_find = f.read()
#                     # Search within XML elements (handle elements without 'id' attribute)
#                     for element in root.findall('record'):  # Assuming 'record' is the element containing data
#                         registration_no = element.find('registration_no').text  # Assuming 'registration_no' is the child element
#                         if text_to_find.lower() in registration_no.lower():
#                             # If no 'id' attribute, use element tag name for reference
#                             if 'id' not in element.attrib:
#                                 element_id = element.tag  # Use the tag name as identifier
#                             else:
#                                 element_id = element.attrib['id']
#                             matches.append(f"{filename} ({xml_file} - Element: {element_id})")  # Include filename, XML file, and element ID (or tag name)
#             except UnicodeDecodeError:
#                 matches.append(f"{filename} (Error: Decoding issue)")
#             except FileNotFoundError:
#                 matches.append(f"{filename} (Error: File not found)")

#     return render_template('result.html', matches=matches, message="Search results")


#this is to display info by taking input
# Path to your XML file
xml_file = 'rider-data-500.xml'

# @app.route('report')
# def index():
#     return render_template('index.html')
# @app.route('fetch_image',methods=['POST'])
# def fetch_images():

@app.route('/fetch_vehicle_details', methods=['GET'])
def fetch_vehicle_details():
    registration_number = request.args.get('registration_number')

    if not registration_number:
        return jsonify({'error': 'Registration number not provided'}), 400

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        vehicle_details = {}
        for record in root.findall('record'):
            if record.find('registration_no').text == registration_number:
                vehicle_details['name'] = record.find('name').text
                vehicle_details['phone_no'] = record.find('phone_no').text
                vehicle_details['address'] = record.find('address').text
                vehicle_details['registration_no'] = record.find('registration_no').text
                break

        if not vehicle_details:
            return jsonify({'error': 'Vehicle not found'}), 404

        return jsonify(vehicle_details)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# #for image rendering
# UPLOAD_FOLDER = 'motorcycle_license_plate-main/riders_pictures'

# # Route to serve images
# from flask import Flask, render_template, send_from_directory
# @app.route('motorcycle_license_plate-main/riders_pictures/<path:filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# from flask import jsonify

# @app.route('/get_images')
# def get_images():
#     # Get list of image filenames in the uploads folder
#     images = os.listdir(UPLOAD_FOLDER)
#     return jsonify(images)
# #the code ends here
# IMAGE_FOLDER = 'motorcycle_license_plate-main/riders_pictures'

# Route to display the list of images
# @app.route('/report')
# def reportt():
#     try:
#         # Get the list of image files in the specified folder
#         image_files = [file for file in os.listdir(IMAGE_FOLDER) if file.endswith(('.jpg', '.jpeg', '.png'))]
#         # Count the number of images
#         num_images = len(image_files)
#         # Generate links to display each image individually
#         image_links = [f"/render/{i+1}" for i in range(num_images)]
#         # Render the template with the list of image links
#         return render_template('report.html', image_links=image_links)
#     except Exception as e:
#         # Return an error message if an exception occurs
#         return jsonify({'error': str(e)}), 500

# # Route to display an individual image
# @app.route('/render/<int:image_index>')
# def render(image_index):
#     try:
#         # Get the list of image files in the specified folder
#         image_files = [file for file in os.listdir(IMAGE_FOLDER) if file.endswith(('.jpg', '.jpeg', '.png'))]
#         # Check if the requested index is valid
#         if 1 <= image_index <= len(image_files):
#             # Get the filename of the image corresponding to the requested index
#             image_filename = image_files[image_index - 1]
#             # Return the template to display the image
#             return render_template('render.html', image_filename=image_filename)
#         else:
#             return 'Image not found!'
#     except Exception as e:
#         # Return an error message if an exception occurs
#         return jsonify({'error': str(e)}), 500
from twilio.rest import Client
account_sid = 'ACb4c3162a42cb3fa401e8e1f3b5ccef7b'
auth_token = '9a7bccfbce611c140fdf55371843b3b6'
twilio_client = Client(account_sid, auth_token)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/fetch_vehicle_details', methods=['GET'])
# def fetch_vehicle_details():
#     # Mock vehicle details based on registration number
#     registration_number = request.args.get('registration_number')
#     vehicle_details = {
#         'name': 'John Doe',
#         'phone_no': '+1234567890',
#         'address': '123 Main Street, City, Country',
#         'registration_no': registration_number
#     }
#     return jsonify(vehicle_details)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    phone_number = request.form.get('phone_number')
    message = request.form.get('message')
    try:
        message = twilio_client.messages.create(
            body=message,
            from_='+18506417136',  # Your Twilio phone number
            to=phone_number
        )
        return jsonify({'success': True, 'message_sid': message.sid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

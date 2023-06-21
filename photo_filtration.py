import os
import shutil
import face_recognition

input_directory = (f"") #put here path of input directory
output_directory = (f"") #put here path of output directory

#create output directory if doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


known_faces_directory = ""        #put here path of know faces directory

known_faces = {}

for file_name in os.listdir(known_faces_directory):
    person_name = os.path.splitext(file_name)[0]
    person_directory = os.path.join(output_directory, person_name)

    if not os.path.exists(person_directory):
        os.makedirs(person_directory)

    image = face_recognition.load_image_file(
        os.path.join(known_faces_directory, file_name))
    face_encodings = face_recognition.face_encodings(image)

    known_faces[person_name] = face_encodings

#iterate over input directory
for file_name in os.listdir(input_directory):
    image_path = os.path.join(input_directory, file_name)

    
    image = face_recognition.load_image_file(image_path)

    
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    #iterate over face encodings in the image
    for face_encoding in face_encodings:
        #compare face encoding with known face encodings
        for person_name, known_face_encodings in known_faces.items():
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)

            if any(matches):
                #copy image to the corresponding directory
                person_directory = os.path.join(output_directory, person_name)
                shutil.copy2(image_path, person_directory)
                print(
                    f"Image '{file_name}' contains a known face ({person_name}) and has been copied to ({person_directory}) directory.")
                break
        else:
            print(
                f"Image '{file_name}' does not contain a known face.")

print("Complete")

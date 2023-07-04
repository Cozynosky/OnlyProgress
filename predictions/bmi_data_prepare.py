from decimal import Decimal
import Augmentor
import pandas as pd
import requests
import os
import cv2

from bs4 import BeautifulSoup

PARENT = "D:/Projects/Magisterka/OnlyProgress/"
PATH_TO_STATIC = "static/data/"
PATH_TO_CSV = PARENT + PATH_TO_STATIC+"datasets/"
PATH_TO_DOWNLOADED = PARENT + PATH_TO_STATIC + "downloaded/"
PATH_TO_ALGORITHMS = PARENT + PATH_TO_STATIC + "face_detection_algorithms/"
PATH_TO_CROPPED = PARENT + "static/data/downloaded/cropped_faces/"

def collect_imgs_data():
    imgs_data = {"height": [], "weight": [], "bmi": [], "url": []}
    
    URL = "https://height-weight-chart.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    a_tags = soup.find("chart").find_all("a")
    
    for i,a in enumerate(a_tags, start=1):
        print_progress("Collecting images data from website",i, len(a_tags))
        
        sub_page_url = a.get("href")
        sub_page = requests.get(URL+"/"+sub_page_url)
        sub_soup = BeautifulSoup(sub_page.content, "html.parser")
        
        body_measurements = sub_soup.find("font")
        height, weight = body_measurements.text.split(", ")
        height = int(height.split(" ")[0]) # height in cm
        weight = int(weight.split(" ")[0]) # weight in kg
        bmi = round(weight / pow(height/100, 2),2)
        
        sub_imgs = sub_soup.find_all("img", class_="largepic")
        
        for sub_img in sub_imgs:
            sub_img_url = URL + "/" + sub_img.get("src")
            imgs_data["height"].append(height)
            imgs_data["weight"].append(weight)
            imgs_data["bmi"].append(bmi)
            imgs_data["url"].append(sub_img_url)
    
    imgs_df = pd.DataFrame(imgs_data)
    imgs_df.to_csv(PATH_TO_CSV+"imgs_data.csv")


def collect_vids_data():
    videos_data = {"height": [], "weight": [], "bmi": [], "url": []}
    
    URL = "https://height-weight-chart.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    a_tags = soup.find("chart").find_all("a")
    
    for i,a in enumerate(a_tags, start=1):
        
        print_progress("Collecting videos data from website", i, len(a_tags))
        
        sub_page_url = a.get("href")
        sub_page = requests.get(URL+"/"+sub_page_url)
        sub_soup = BeautifulSoup(sub_page.content, "html.parser")
        
        body_measurements = sub_soup.find("font")
        height, weight = body_measurements.text.split(", ")
        height = int(height.split(" ")[0]) # height in cm
        weight = int(weight.split(" ")[0]) # weight in kg
        bmi = round(weight / pow(height/100, 2),2)
        
        sub_videos = sub_soup.find_all("video")
                   
        for video in sub_videos:
            viedo_url = URL + "/" + video.find("source").get("src")
            videos_data["height"].append(height)
            videos_data["weight"].append(weight)
            videos_data["bmi"].append(bmi)
            videos_data["url"].append(viedo_url)
    
    additional_videos_url = URL + "/videos/heightweight_videos.html"
    vid_page = requests.get(additional_videos_url)
    vid_soup = BeautifulSoup(vid_page.content, "html.parser")
    a_vid_tags = vid_soup.find_all("a")[:-2]
    
    for i, a_vid_tag in enumerate(a_vid_tags, start=1):
        
        print_progress("Collecting additional videos data from website", i, len(a_vid_tags))
        
        a_href = a_vid_tag.get("href")
        sub_vids_page = requests.get(URL+"/videos/"+a_href)
        sub_vids_soup = BeautifulSoup(sub_vids_page.content, "html.parser")
        
        if sub_vids_page.status_code == 200:
            body_measurements = sub_vids_soup.find("h1")
            height = body_measurements.text.split(" ")[0][:-1]
            height_foots = Decimal(height.split("'")[0]) * Decimal(30.48)
            height_inches = Decimal(height.split("'")[1]) * Decimal(2.54)
            height = round(height_foots + height_inches)
            weight = round(Decimal(body_measurements.text.split(" ")[1]) * Decimal(0.45359237))
            bmi = round(weight / pow(height/100, 2),2)
            
            sub_vids = sub_vids_soup.find_all("source")
            
            for vid in sub_vids:
                video_url = URL+"/videos/"+vid.get("src")
                if not video_url in videos_data["url"]:
                    videos_data["height"].append(height)
                    videos_data["weight"].append(weight)
                    videos_data["bmi"].append(bmi)
                    videos_data["url"].append(video_url)
    
    vids_df = pd.DataFrame(videos_data)
    vids_df.to_csv(PATH_TO_CSV + "vids_data.csv")
  

def download_imgs():
    data = pd.read_csv(f"{PATH_TO_CSV}imgs_data.csv")
    download_path = f"{PATH_TO_DOWNLOADED}imgs/"
    
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    for index, row in data.iterrows():
        print_progress("Downloading images", index+1, len(data))
        img = requests.get(row["url"]).content
        img_name = row["url"].split("l/")[1]
        bmi = row["bmi"]
        
        if bmi < 18.5:
            folder_name = "under_weight"
        elif bmi < 24.9:
            folder_name = "normal_weight"
        elif bmi < 29.9:
            folder_name = "over_weight"
        elif bmi < 34.9:
            folder_name = "obese_class_I"
        elif bmi < 39.9:
            folder_name = "obese_class_II"
        else:
            folder_name = "obese_class_III"
            
        folder_path = f"{download_path}{folder_name}/"
            
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(f"{folder_path}{img_name}", "wb") as f:
            f.write(img)
    

def download_videos():
    data = pd.read_csv(f"{PATH_TO_CSV}vids_data.csv")
    download_path = f"{PATH_TO_DOWNLOADED}vids/"
    
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    for index, row in data.iterrows():
        print_progress("Downloading videos", index+1, len(data))
        vid_page = requests.get(row["url"])
        if vid_page.status_code == 200:
            vid_name = row["url"].split("/v/")[1]
            bmi = row["bmi"]
            
            if bmi < 18.5:
                folder_name = "under_weight"
            elif bmi < 24.9:
                folder_name = "normal_weight"
            elif bmi < 29.9:
                folder_name = "over_weight"
            elif bmi < 34.9:
                folder_name = "obese_class_I"
            elif bmi < 39.9:
                folder_name = "obese_class_II"
            else:
                folder_name = "obese_class_III"
                
            folder_path = f"{download_path}{folder_name}/"
                
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            with open(f"{folder_path}{vid_name}", "wb") as f:
                f.write(vid_page.content)


def make_photos_from_vids():
    data_path = PATH_TO_DOWNLOADED + "vids/"
    save_path = PATH_TO_DOWNLOADED + "imgs_from_vids/"
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    folders = os.listdir(data_path)
    
    total_vids = 0
    completed_vids = 0
    
    for folder in folders:
        for path in os.scandir(data_path+folder):
            total_vids += 1
    
    for folder in folders:
        folder_path = data_path+folder+"/"
        save_folder_path = save_path + folder+"/"
            
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            
        vid_names = os.listdir(folder_path)
        
        for vid_name in vid_names:
            vid_path = folder_path + vid_name
            
            vid_cap = cv2.VideoCapture(vid_path)
            fps = int(vid_cap.get(cv2.CAP_PROP_FPS))
            
            success, image = vid_cap.read()
            frame = 1
            while success:
                if frame % (fps//2) == 0:
                    cv2.imwrite(f"{save_path}{folder}/{vid_name}_frame_{frame}.jpg", image)
                success, image = vid_cap.read()
                frame += 1
                
            completed_vids += 1
            print_progress("Making photos from videos", completed_vids, total_vids)
  

def crop_faces(margin: float):
    paths_to_imgs = [PATH_TO_DOWNLOADED + "imgs/", PATH_TO_DOWNLOADED + "imgs_from_vids/"]
    cropped_faces_path = PATH_TO_DOWNLOADED + "cropped_faces/"
    
    total_imgs_count = 0
    found_faces_count = 0
    curr_img = 1
    
    
    for path in paths_to_imgs:
        for child in os.listdir(path):
            child_path = path + "/" + child + "/"
            for img in os.scandir(child_path):
                total_imgs_count += 1
    
    if not os.path.exists(cropped_faces_path):
        os.makedirs(cropped_faces_path)
    
    for path in paths_to_imgs:
        for child in os.listdir(path):
            child_path = path + child + "/"
            for img_name in os.listdir(child_path):
                print_progress("Finding faces", curr_img, total_imgs_count)
                img_path = child_path + img_name
                img = cv2.imread(img_path)
                if len(found_faces := find_face(img, margin)) == 1:
                    found_faces_count += 1
                    x1, y1, x2, y2 = found_faces[0]
                    
                    cropped_img = crop_image_to_dimensions(img, x1, y1, x2, y2)
                    cropped_img_path = cropped_faces_path + child
                    
                    if not os.path.exists(cropped_img_path):
                        os.makedirs(cropped_img_path)
                    
                    cv2.imwrite(cropped_img_path + "/cropped_" + img_name, cropped_img)
                    

                curr_img += 1
    
    print(f"images: {total_imgs_count}, faces: {found_faces_count}")
        

def find_face(img, margin):
    algorithm_path = PATH_TO_ALGORITHMS + "haarcascade_frontalface_default.xml"
    
    haar_cascade = cv2.CascadeClassifier(algorithm_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    frontal_faces = haar_cascade.detectMultiScale(gray_img, 1.3, 5)
    results = []
    
    for (x,y,w,h) in frontal_faces:
        margin_x = int(w * margin)
        margin_y = int(h * margin)
        x1 = x - margin_x
        x2 = x + w + margin_x
        y1 = y - margin_y
        y2 = y + h + margin_y
        
        results.append((x1, y1, x2, y2))
    
    return results
  
        
def crop_image_to_dimensions(img, x1, y1, x2, y2):
    if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
        img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
    return img[y1:y2, x1:x2, :]


def pad_img_to_fit_bbox(img, x1, x2, y1, y2):
    img = cv2.copyMakeBorder(img, - min(0, y1), max(y2 - img.shape[0], 0),
                             -min(0, x1), max(x2 - img.shape[1], 0), cv2.BORDER_REPLICATE)
    y2 += -min(0, y1)
    y1 += -min(0, y1)
    x2 += -min(0, x1)
    x1 += -min(0, x1)
    return img, x1, x2, y1, y2


def augumente_data():
    for folder in os.listdir(PATH_TO_CROPPED):
        folder_path = PATH_TO_CROPPED + folder + "/"
        
        p = Augmentor.Pipeline(source_directory=folder_path, output_directory=folder_path)
        p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
        p.flip_left_right(probability=0.5)
        p.random_distortion(probability=0.25, grid_width=2, grid_height=2, magnitude=8)
        p.random_color(probability=1, min_factor=0.8, max_factor=1.2)
        p.random_contrast(probability=.5, min_factor=0.8, max_factor=1.2)
        p.random_brightness(probability=1, min_factor=0.5, max_factor=1.5)
        
        p.sample(300)


def print_progress(process_name,curr, total):
    os.system('cls' if os.name=='nt' else 'clear')
    
    percent = round(curr / total * 100,2)
    completed = int(percent)
    to_compish = 100 - completed
    print(process_name)
    print(f"[{'#' * completed}{'-' * to_compish}] {percent}% - {curr}/{total}")
   

if __name__ == "__main__":
    #collect_imgs_data()
    #collect_vids_data()
    download_imgs()
    download_videos()
    make_photos_from_vids()
    crop_faces(0.1)
    augumente_data()
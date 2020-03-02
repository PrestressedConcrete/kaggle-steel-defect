import os
import csv
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
import copy as cp
import matplotlib.image as mpimg
## Read and save CSV
def CSV_to_descriptions(csv_path): # dictionnary with names and captions of images
    'convert csv train and test files into usable dictionnary'

    # first dictionnary 
    descriptions_dict = {}
    
    #open training file
    with open(csv_path,'r') as csvfile:
        # split by ,
        file_reader = csv.reader(csvfile,delimiter=',',)

        #ignore first entry
        iter_file_reader = iter(file_reader)
        next(iter_file_reader)

        # 4 types of fdefects 
        compteur = 0

        # fill in dictionnary with all captions
        for row in iter_file_reader:
            # extract image id
            img_name = row[0].split('_')[0]
            img_name = img_name.split('.')[0]

            # create empty list
            if (compteur%4==0):
                descriptions_dict[img_name] = []

            # add caption
            caption = row[1]
            descriptions_dict[img_name].append(caption)

            # update compteur
            compteur +=1
        #iterate over images
    for img_name in descriptions_dict.keys():

        ## start converting captions to list of integres

        # get raw data
        caption_list = cp.copy(descriptions_dict[img_name])

        # defect number
        count = 0

        #iterate of defects type
        for string in caption_list:
            # convert string to list of integers
            if (caption_list[count] == ''):
                caption_list[count] = []
            else:

                # convert to integer
                caption_list[count] = string.split(' ')
                caption_list[count] = [int(number) for number in caption_list[count]]

                # delete 1 on all indices to match python indices
                for i in range(0,len(caption_list[count]),2):
                    caption_list[count][i] += -1
                    
            #update dictionnary
            descriptions_dict[img_name] = caption_list
            
            #update count
            count+=1
    return descriptions_dict

def check_image_size(descriptions_dict,DIR):
    'check if all images are the same size'
    #compteur image
    compteur = 0

    #iterate over img names
    for img_name in descriptions_dict.keys():
        # update image number
        compteur +=1

        # convert image to array
        img_path = os.path.join(DIR,img_name+'.jpg')
        img = Image.open(img_path)
        #img = PIL.Image.open(img_path).convert("L")
        imgarr = numpy.array(img)

        # verification
        if (imgarr.shape != (256,1600,3)):
            print('Problème with '+ img_name)
            print(imgarr.shape)

    # retourner le nombre d'image, expected 12568
    print(compteur)

def description_to_image(img_name,descriptions_dict,img_directory_path = "",plot_image = False):

    
    'convert segmentation in csv file into numpy image'
    
    #image_size
    img_size = (256,1600)

    #initialize final list, 0 is the default value
    image = np.zeros(img_size)
    
    #take values
    caption_list = cp.deepcopy(descriptions_dict[img_name])
    ## fill in the list from top to bottom, and left to right
    #iterate on defects type
    for defect_number in range(4):
        #iterate on the lists of defects
        for compteur,value in enumerate(caption_list[defect_number]):
            # if pair : pixel, else : length
            if (compteur%2==0):
                # on remplis tous les autres jusqu'a defect size:
                for compteur2 in range(caption_list[defect_number][compteur+1]):
                    #take position of the pixel
                    current_state = value-1+compteur2
                    
                    #convert into row and column (top to bottom and left to right)
                    row = current_state%img_size[0]
                    column = current_state//img_size[0]
                    
                    # add defect number
                    image[row][column]=defect_number+1
    
                    
    #plot both of the images
    if(plot_image):
        array = image
        print(array.max())
        plt.imshow(array)
        plt.show()
        img = mpimg.imread(os.path.join(img_directory_path,img_name+'.jpg'))
        plt.imshow(img)
        print(img.shape)
        plt.show()
    else:
        return image
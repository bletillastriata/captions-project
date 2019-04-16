"""
Usage: 
Import and instantiate with the path to the images as a parameter. Then call generate_data() function, 
passing in an augmenter, the number of augmentations desired (will be used to determine ratio of augmentations), 
and batch size desired. It is expected that each image-caption pair is in its own folder with each folder name 
being the number of the pair.

See data_preprocessor_example.ipynb for a walkthrough.

"""

class ImagePreprocessor(object):
    
    def __init__(self, path_to_input_images):

        if not os.path.exists(path_to_input_images):
            
            raise ValueError('path(s) doesn\'t exist!')
        self.input_root, self.input_folders, self.input_files = next(os.walk(path_to_input_images))
    
        
    def load_data_from_file(self, index):
        img_filepath = os.path.join(self.input_root, index,"img.jpg.jpg")
       
        # use skio to read the image
        img =  skio.imread(img_filepath)
        txt_filepath = os.path.join(self.input_root, index,"text.txt.txt")
        
        # read and save the text file into a variable
        with open(txt_filepath,'r') as file:
          text = file.read()
        
        # return image and its corresponding caption
        return img, text


    def augment_data(self, augmenter,img_batch, num_augs):
 
        # create list to hold augmented images
        aug_imgs = []
        
        # Augment each image in the batch and add the augmented image to aug_imgs
        for img in img_batch:
          augmented_image = augmenter.augment_image(img)
          aug_imgs.append(augmented_image)
          
        # convert aug_imgs to numpy array and then return it
        aug_imgs = np.array(aug_imgs)
        return aug_imgs
                      
    def generate_data(self, augmenter, num_augs, batch_size):
        images = self.input_folders
        #print(str(images))
  
        # create augmenter with probability determined by num_augs
        augmenter = iaa.Sometimes(num_augs/(num_augs + 1), augmenter)
         
        i = 0
        shuffle(images)
        
        while True:
            if i >= len(images):
              i = 0
              shuffle(images)
                
            #create list to hold images for batching
            img_batch = []
            caption_batch = []
            
            # create a batch of images 
            for j in range(i,min(i+batch_size, len(images))):
              raw_img, caption = self.load_data_from_file(images[j])
            
              # add captions to the batch
              caption_batch.append(caption)

              # Resize the images to 2000 * 2000
              resized_img = cv2.resize(raw_img,(2000,2000))
              img_batch.append(resized_img)
              
            # yield batches of captions and images (with some images augmented)
            yield caption_batch, self.augment_data(augmenter,img_batch,num_augs)
            i += batch_size
          

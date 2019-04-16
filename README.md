# T2-Dont-Set-Us-on-FIRE _(the Phyromaniacs)_
_Siyuan Peng, Anyesha Majumdar, Logan Marks, Su Lan Mair_

_Faculty Advisor: Dr. Dave Levin_ 

_Research Educator: Dr. Raymond Tu_

_Peer Mentors: Derek Zhang, Timothy Lin_

## Google Conceptual Captions Challenge


The goal of this challenge is to train a model to generate accurate and natural-sounding captions for images it has never seen before. This is accomplished by training the model on a training set of just over 3.3 million image-caption pairs and validating on a set of just under 16,000. For more on the dataset, see [the Google AI Blog](https://ai.googleblog.com/2018/09/conceptual-captions-new-dataset-and.html) or [view the paper directly](https://aclweb.org/anthology/P18-1238).

## Requirements
In order to run the scripts we have provided, you will want to make sure you have the following modules installed:
```python
imgaug
matplotlib
multiprocessing.pool
numpy
os
pandas
random
requests
shutil
skimage.io
```
These can be installed using pip or anaconda with Requirements.txt (provided in this repository). Also note that for this project, we recommend using a virtual environment so that any changes you make do not affect your existing python configuration. We recommend either [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or [pipenv](https://pipenv.readthedocs.io/en/latest/install).  

## Downloading the Data
_Note: the current version of the downloader runs best with **at least 8GB** of RAM. A version that uses less memory and fewer resources is currently in development._

Using the downloader_vers1.py requires at most three directories: one for images whose responses confirm they are JPEG images, one for images whose responses do not confirm they are JPEG images (i.e., their response returns "None" even though they may still be images), and one for storing the error log. For each image, the downloader will save the image alongside its caption (as a .txt file) in a folder labeled with the image's index number. 

To download the data using downloader_vers1.py, first download the training split tsv file from [the competition page](https://ai.google.com/research/ConceptualCaptions) by clicking the button labeled "Training Split". Then download the downloader_vers1.py file from this repository.

Create two folders in your path: one for jpeg files and one for none-jpeg files. The names of these files are not important as long as you know what they are.

Open downloader.py and edit it according to the following:

In the following line, put the path to the tsv (from your local computer) in place of the XXX.
```python
training_file_dir: str = XXX
```

In the following line, put the path to the jpeg image folder (as a string) in place of the XXX.
```python
jpeg_folder_path: str = XXX
```

In the following line, put the path to the non-jpeg image folder (as a string) in place of the XXX.
```python
none_jpeg_folder_path: str = XXX
```

In the following line, put the path where you could like to save the error log.
```python
error_log_path: str = XXX
```

In the following line, define the maximum number of images you want to download (as an int) in place of the XXX.
```python
max_image_num: int = XXX
```

In the following line, define the starting position for downloading in place of XXX. If this is the first time you're running thescript, this will be 0.
```python
start_pos: int = 0
```

In the following line, define the maximum number of threads for downloading in place of XXX. The number of threads will be XXX + 1.
```python
max_concurrent_download: int = XXX
```
Save downloader_vers1.py. You can now run it to download the images, either on an instance or on your local machine. We advise ensuring you have 500 - 550GB to store the data.

## Generating Data
_Note: This preprocessor was built to go along with the current version of the downloader (downloader_vers1.py). A more lightweight version of the downloader is in development. Once development is complete, this preprocessor will also be updated. The legacy versions of both the downloader and the preprocessor will remain available but will not be supported by future developments in this project._

Download and import data_preprocessor.py (see below) to generate data. 
```python
import data_preprocessor as preprocessor
example = ImagePreprocessor(path/to/images)
```
Notice that this preprocessor assumes the user has already defined an augmenter tailored to the user's needs. For a walkthrough about how this is done using data_preprocessor.py, download  the script and the notebook data_preprocessor_example and then run the notebook. Images in the example are augmented using a variety of techniques from the [imgaug library](https://github.com/aleju/imgaug) including adding noise, blur, dropout, affine, sharpening, and contrast normalisation. 


As shown in data_preprocessor_exampls.ipynb, the generator can then be used to generate data as follows:
```python
i = 0 # allows us to iterate through captions and images in one loop
for caption_batch, img_batch in example.generate_data(augmenter, num_augs, batch_size):
    for img in img_batch:
        print(caption_batch[i])
        plt.imshow(img)
        plt.grid(False) # optional; removes gridlines from image
        plt.show() 
        print("\n") # optional; added for spacing purposes only
        i += 1
    i = 0
    print("End of batch \n \n") # optional; used for clarity during testing
            

```


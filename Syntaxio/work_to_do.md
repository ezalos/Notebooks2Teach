# Missing from the course

- Python Positionning
  - Overview: 1 slide par tool 
    - agate
    - bokeh
    - pybrain
    - tensorflow
    - keras
    - mxnet
    - caffe
- Calculations and Graphs
  - Basemap is absent in matplotlib
  - ...
- Relational Data Manipulation
  - h5py
  - netCDF
  - ...
- Introduction to Open-cv:
  - Image Thresholding
  - Edge detection
  - Contour Detection
- Machine Learning & Deep Learning
  - Mxnet / caffe
  - PyTorch / TensorFlow:
    - Full neuralnet pre-training :
      - COURSE: Full training of MNIST
      - EXERCISE: Full training of FashionMNIST
    - Automatic neural net HP search:
      - gridsearch
      - optuna
    - Fine-tuning :
      - vgg / resnet
      - EXERCISE: Satellite imagery classification, from finetuning
  - Pytorch courses ideas:
    - finetuning
    - transfer learning
    - data augmentation
	- hyper-parameter search
	- ...


# 

Translate this notebook cell in english, it most generally is in markdown format. Do NOT add any '#' at the beginning of a line, just keep the ones already present, but DO NOT ADD ANY NEW '#' AT ALL.

If necessary do not hesitate to add some formatting to the text and line breaks to make it more readable.


Improving the course:
- pandas practice exercises in the middle 
- sklearn, add house prices, and maybe direct a more results orientend EDSA / training, with some iteration in the class.
  - Start from a general methodology to be followed, (present it at the beginning, and then follow it for each chapter).
    - Check type of problem
    - Check data, especially for missing values, outliers, and for pbms
    - check target variable correlation / relathionship with other variables
    - Train as fast as possible a baseline model
    - Check for errors / performance
    - Iterate to improve performance (other models / HP / feature engineering...)
  - Also, work on the explanation of each algorithms, and presents it's assumptions / Hyper Parameters
- for pytorch, work on 
  - Underlying library concepts (gradient / optimizer)
  - Explanation of each layer
  - How to choose the right optimizer / loss function
  - Accessing the model layers
[![Vietnamese](https://img.shields.io/badge/lang-vi-blue)](https://github.com/gnurt2041/Football-Match-Analysis/blob/main/README.vi.md)
# An application of Yolov5 and ByteTrack in football match analysis based on broadcast video
The objective of the project is to identify and track four objects: player, referee, goalkeeper and ball. Then, based on the inertial algorithm, I calculate the percentage of ball possession between the two teams in the match video.
# Model training
All the training codes with YoloV5 are in the [train.ipynb](https://github.com/gnurt2041/Football-Match-Analysis/blob/main/train.ipynb). It includes how to download the my dataset with about 2800 images and some arguments for the training progress.

My training progress was running on Google Colab Pro with high-ram (25GB) (If possible, I recommend using this high-ram configuration to help reduce bottelneck when loading data to the GPU). My training is continuous, so each full 300 epochs training would take 55 hours on Tesla T4 16GB and 27 hours on A100 40GB.

After fully training the Yolov5 model, the results should look like this:
<p align="center">
<img src="https://github.com/gnurt2041/Football-Match-Analysis/blob/4b39d76c577854f8427937c4bfab6149aeada152/image/yolov5_demo.png" width="1920px" length="1080px"></a>
</p>

# Model inference and annotation results

All the inference code with Yolov5, ByteTrack combined with my algorithm using HSV color filter and inertial algorithm are in the [main.ipynb](https://github.com/gnurt2041/Football-Match-Analysis/blob/main/main.ipynb). The detail of my algorithm is in the [football](https://github.com/gnurt2041/Football-Match-Analysis/tree/main/football) folder in this repository.

Here is a short demo of the final result of this project: 

https://github.com/gnurt2041/Football-Match-Analysis/assets/71776470/2c78633c-8965-4183-8ef4-b60dccada326


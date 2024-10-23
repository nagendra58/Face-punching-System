import cv2
import face_recognition
import numpy as np
import pandas as pd
import datetime
import os
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# Set up directories for images and data
if not os.path.exists('employee_faces'):
    os.makedirs('employee_faces')

if not os.path.exists('attendance_logs'):
    os.makedirs('attendance_logs')
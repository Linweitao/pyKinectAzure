import json

import cv2
import numpy as np
from matplotlib import pyplot as plt

from pykinect_azure import pykinect, k4abt_body2D_t, k4abt_body_t
from src.tool import Camera3dTo3dCoordinateConversion, twoPoseVisCompare


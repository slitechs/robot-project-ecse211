from math import *
def normalize(R, G, B):
    """Normalize RGB values."""
    total = R + G + B
    if total == 0:
        return 0, 0, 0  # To avoid division by zero
    red = R / total
    green = G / total
    blue = B / total
    return red, green, blue

def distance(X,Y,Z, R,G,B):
    return sqrt((X-R)**2 + (Y-G)**2 + (Z-B)**2)

# return the closest color as a string
def classify_left(measured):
    """Classify the color of the measured RGB values."""
    # Normalize the measured RGB values
    normalized_measured = normalize(*measured)
    
    centroids = {
        'black': [0.284, 0.399, 0.313],
        'blue': [0.339, 0.383, 0.279],
        'red': [0.793, 0.125, 0.085]
    }
    
    # Initialize minimum distance and classification
    min_distance = float('inf')
    classification = None
    
    # Iterate through centroids to find the closest one
    for color, centroid in centroids.items():
        dist = distance(*centroid, *normalized_measured)
        if dist < min_distance:
            min_distance = dist
            classification = color
    return classification

def classify_right(measured):
    """Classify the color of the measured RGB values."""
    # Normalize the measured RGB values
    normalized_measured = normalize(*measured)
    
    centroids = {
        'black': [0.286, 0.453, 0.259],
        'blue': [0.301, 0.425, 0.270],
        'red': [0.766, 0.153, 0.08]
    }
    
    # Initialize minimum distance and classification
    min_distance = float('inf')
    classification = None
    
    # Iterate through centroids to find the closest one
    for color, centroid in centroids.items():
        dist = distance(*centroid, *normalized_measured)
        if dist < min_distance:
            min_distance = dist
            classification = color
    return classification

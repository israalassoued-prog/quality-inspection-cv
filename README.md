# Automated Quality Inspection (Computer Vision)

A Python + OpenCV pipeline that automatically inspects images of parts and classifies them as **PASS** or **FAIL** based on structural defects, simulating an automated optical inspection (AOI) system used on industrial production lines.

Built as part of the **Robotics & Automation Industrial Training Kit — Project 2**, DecodeLabs (2026 batch).

## What it does

The script takes an image of a part (in this case, hand-drawn circular "gear-like" shapes), processes it through a computer vision pipeline, and decides whether the part is defective by measuring how much its outline deviates from a perfect convex shape. Any deviation beyond a calibrated threshold is flagged as a structural defect, marked with a bounding box, and the part is rejected.

## How the pipeline works

1. **Pre-processing**
   - Convert image to grayscale
   - Apply Gaussian Blur to suppress noise
   - Apply binary thresholding to isolate the part's silhouette

2. **Topology analysis**
   - `cv2.findContours` traces the outer boundary of the shape
   - `cv2.convexHull` computes the smallest convex shape enclosing that boundary
   - `cv2.convexityDefects` measures the gap between the actual contour and the convex hull at every point

3. **Tolerance gate (decision logic)**
   - Each defect's raw distance is corrected (`distance / 256.0`, per OpenCV's fixed-point scaling)
   - Distances are compared against a calibrated threshold (`THRESHOLD_MAX`), set above the natural noise floor measured from known-good parts
   - The single largest defect per image is tracked
   - If it exceeds the threshold → **FAIL**, and a red bounding box is drawn at the defect location
   - Otherwise → **PASS**

4. **Batch evaluation**
   - The script processes every image in `my_folder/`
   - Compares its prediction against the ground truth encoded in each filename (`good*.png` / `bad*.png`)
   - Saves each processed image (with bounding box, if defective) to `output/`
   - Reports overall sorting accuracy

## Results

Tested on a 20-image dataset (10 known-good parts, 10 known-defective parts):

```
20 out of 20 correct
```

## Requirements

- Python 3
- OpenCV (`opencv-python`)
- NumPy

Install dependencies:

```bash
pip install opencv-python numpy
```

## Usage

1. Place test images inside `my_folder/`. Filenames must contain `"good"` or `"bad"` so the script can score itself against ground truth (e.g. `good1.png`, `bad1.png`).
2. Run the script:

```bash
python inspect.py
```

3. Processed results (with bounding boxes drawn on defective parts) are saved to `output/`.

## Project structure

```
.
├── inspect.py       # main pipeline script
├── my_folder/       # input images (10 good, 10 defective)
└── output/          # generated results (created automatically, not tracked in git)
```

## Notes / known limitations

- This implementation is calibrated for **closed, mostly-convex shapes** (e.g. gears, washers, simple parts). Very large or topologically "open" defects (e.g. a shape with a fully broken edge rather than a localized dent) can behave unpredictably, since convexity-defect detection assumes a largely intact closed contour.
- The threshold (`THRESHOLD_MAX`) was calibrated empirically by measuring the natural noise floor on known-good images before testing on defective ones, rather than chosen arbitrarily.

## What this project demonstrates

- Image pre-processing (grayscale, blur, thresholding) with OpenCV
- Contour and shape analysis (convex hulls, convexity defects)
- Threshold-based pass/fail decision logic calibrated from real measurements
- Batch processing and automated accuracy evaluation against ground truth

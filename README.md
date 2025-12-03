
# EcoInnovators Ideathon 2026: AI-Powered Rooftop PV Detection 

##  Project Overview
This solution is an automated AI pipeline designed to detect rooftop solar photovoltaic (PV) installations from high-resolution satellite imagery. Developed for the **EcoInnovators Ideathon 2026**, it assists in the governance of the *PM Surya Ghar: Muft Bijli Yojana* scheme by verifying solar installations at reported GPS coordinates.

The system uses a **YOLOv8-Medium** model for detection and implements a precise **Geospatial Buffer Zone Logic** (1200 sq.ft vs 2400 sq.ft) to validate beneficiary claims.

---

##   IMPORTANT: Large File Downloads
Due to GitHub's file size limits, the full trained model weights and comprehensive project datasets are hosted externally. Please access them here:

*  Full Project Drive (Datasets & Logs): [Click Here to Access Google Drive](https://drive.google.com/drive/folders/1tF_6N7mysWNyQUnvSvSagke8fzV1Ox0N?usp=drive_link)
*  Trained Model File (`solar_model.pt`): [Click Here to Download Model](https://drive.google.com/drive/folders/1yyUTGWSUplc2gUg1uDnsV5SWqgsEDoaj?usp=drive_link)

---

##  Key Features
* **AI Detection:** Utilizes a custom-trained `YOLOv8m` model to identify solar panels in satellite imagery (Zoom Level 18-19).
* **Buffer Verification:** Strictly adheres to the challenge rules by checking:
    * **Inner Ring:** 1200 sq.ft radius (~6m).
    * **Outer Ring:** 2400 sq.ft radius (~8.4m) if the first check fails.
* **Area Estimation:** Dynamically calculates Ground Sample Distance (GSD) based on latitude to provide accurate area quantification in square meters ($m^2$).
* **Audit-Ready:** Generates visual evidence (overlay images) and a structured JSON report for every sample.
* **Dockerized:** Fully containerized for consistent deployment across any environment.

##  Repository Structure
```

├── Pipeline code/          \# Core Python scripts for inference
├── Environment details/    \# requirements.txt and setup info
├── Trained model file/     \# Contains the YOLOv8 model (or link to it)
├── Artefacts/              \# Sample output images (Overlays)
├── Prediction files/       \# Final JSON submission output
├── Dockerfile              \# Configuration for building the Docker image
├── main.py                 \# Entry point for the application
└── input\_sites.xlsx        \# Input data with Sample ID, Lat, Lon

````

##  Installation & Usage

### Method 1: Python (Local)
1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Place the Model:**
    Download `solar_model.pt` from the Drive link above and place it in the root directory.
4.  **Run the Pipeline:**
    ```bash
    python main.py
    ```
    *Results will be saved in the `outputs/` folder.*

### Method 2: Docker (Recommended)
This application is containerized for easy submission and testing.

1.  **Build the Image:**
    ```bash
    docker build -t solar-detector .
    ```
2.  **Run the Container:**
    ```bash
    docker run -v $(pwd)/outputs:/app/outputs solar-detector
    ```

##  Logic & Methodology
1.  **Input:** Reads `input_sites.xlsx` containing `sample_id`, `latitude`, and `longitude`.
2.  **Acquisition:** Fetches a 600x600 satellite image via API (Google Maps Static / MapTiler).
3.  **Inference:** YOLOv8 detects bounding boxes for solar panels.
4.  **Geometry Check:** `Shapely` library creates polygon buffers around the image center.
    * If a panel intersects the **1200 sq.ft** buffer -> **VERIFIABLE**.
    * Else if it intersects the **2400 sq.ft** buffer -> **VERIFIABLE**.
    * Otherwise -> **NOT_VERIFIABLE**.
5.  **Output:** Saves a `submission.json` and annotated `.jpg` images.



* **Model Architecture:** Ultralytics YOLOv8
* **Geospatial Logic:** Shapely & OpenCV
* **Data Sources:** Roboflow Public Datasets
````
##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

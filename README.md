# **Project Title: Textile Design Search System**

## Description
Textile Design Search System is a software solution developed to address the challenge of finding similar textile designs from a vast local database. The system utilizes image processing techniques and search algorithms to enable efficient searching and matching of textile designs. With this system, manufacturer like Salasar Fashion can enhance their design selection process, save time, and improve productivity.

The Textile Design Search System utilizes advanced image processing techniques and search algorithms to analyze and compare textile designs based on visual features. The system leverages the chi-squared (chi2) distance metric to measure the similarity between designs. This distance metric captures the dissimilarity between the histograms of color and texture features extracted from the designs. The system employs OpenCV library for image processing tasks and custom algorithms for search and matching operations, incorporating the chi2 distance calculation for accurate and efficient design retrieval.

I undertook contract that helped Salasar Fashion, a pioneer in Textile Industry to help them search similar textile designs from their root design database of nearly 2TB size, and 1,00,000+ images.

## Prerequisites
* Python 3.7 upto 3.10
* Flask web framework
* OpenCV library
* NumPy library

## Installation
1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/harsh-sutariya/design_search.git
   ```
2. Create a virtual environment
   ```
   py -m venv venv
   ```
3. Activate the virtual 
   ```bash
   venv/Scripts/activate
   ```
4. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Example
To demonstrate the functionality of the Textile Design Search System, follow these steps:

1. Start the application by running the app.py file.
2. Access the system through a web browser by entering the URL http://localhost:5000.
3. Place your directory of images in 'files/static/dataset/' folder
4. Index images
5. Upload a design image using the "Upload a Design" form.
6. Specify the number of similar images to display.
7. Click the "Search" button.
8. The system will process the uploaded image and retrieve the most similar designs from the database.
9. The search results will be displayed, showing the similar designs along with their distances and paths.

## Contributing
If you encounter any issues or have suggestions for improvements, please request a push and drop a mail.

## Contact
For any inquiries or further information, please contact at:

Email: harshsutariya1179@gmail.com

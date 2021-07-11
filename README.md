# w251-project-door-camera
Final project for W251- Steven Leung, Juan Ramirez, Javed Roshan

# Files and Directories (prelim)


- body_detection.ipynb: detects human bodies from images using opencv hogdetector
- body_detection.py: same thing in a py script

- image\_collection\_youtube.ipynb: takes youtube search query and writes frame images to folder 'youtube_scraping'

- image\_collection.py: script that takes url (need to automate) and downloads from google images into folder 'google_image_scraping'. Leaning away from this and towards youtube solution

- face_rec.py: recognizes individuals based on their face in images or on live feed.



- **Folder:** facial\_rec\_images: images to test face\_rec.py on

- **Folder:** google\_image\_scraping
	- repo with folders from google image scraping script above

- **Folder:** youtube\_scraping
	- top-level: videos downloaded through notebook above
	- vid\_to\_images.ipynb: converts mp4 vids to images and stores in vid\_to_image folder
	- **Folder:** vid\_to_image
		- top-level: raw images from videos above
		- body\_detection\_youtube.ipynb: detects human bodies from images and stores cropped images in cropped\_ppl folder
		- **Folder:** cropped_ppl
			- cropped images of ppl (THIS NEEDS WORK)
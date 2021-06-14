# facewebapi
Python Face Recognition Web API Django

run the program with command

"python manage.py runserver"

go to http://localhost:8000/faceapi/
and you will see
--------------------------------------------------
First, upload all known images to the server.
Server images will be mark as known images.
Upload only one person's face in a image
'''http://localhost:8000/faceapi/upload?name={Person_Name}&img={filename/jpg}'''

Compare your test image with the server images.
The unknown image will be compared to all known images that have been uploaded to the server.
'''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
---------------------------------------------------

First, fill the server with KNOWN IMAGES. Only submit one face in a image
'''http://localhost:8000/faceapi/upload?name={Person_Name}&img={filename/jpg}'''
you can pass the 'name, img' arguments
which is 'name' for person name
and 'img' for the image url that you can find in the internet

Now, you can compare THE_UNKNOWN_IMAGE with THE_KNOWN_IMAGES
'''http://localhost:8000/faceapi/compare?img={filename.jpg}'''
img argument is the image's url

it will return json response like:
__________________________________
{
  detected: [
    "arief"
  ],
  response_time: 3.160721778869629
}
__________________________________
in detected it will return array that means you can detect multiple face in a image

NOTE: The first time you compare must be slow in response_time. But, after caching (i did it with pickle) it will run faster

# Neulandeuphonie

<h3 style="color: #4183c4; text-align: center;">The world is facing the abyss! For those of us who absolutely can't handle that, there's now Neulandeuphonie!</h3>

## What is it?
Neulandeuphonie is a censoring proxy that replaces bad words with good ones and all images with images of cats (everybody loves cats). This change in site demonstrates how easy it is to manipulte website and how people need to live in counries which are known for blocking (e.g. the majority of China).

## Installing
To install it is recommended to create a python2 virtualenv (env/ is already in .gitignore) and activate it. You have to install the virtualenv tool. Most distributions have it in packages named ```python-virtualenv``` or similar. 

    virtualenv --python python2 env # create virtualenv
    source env/bin/activate

After that you can install the dependencies from the requirements.txt via

    pip install -r requirements.txt
    
## Running it
To run neulandeuphonie you simply start the proxy by executing
    
    mitmdump -s neulandeuph.py

It will start a proxy on *:8080 which you can set in your browser.

## Examples

![Example](https://github.com/Jugendhackt/neulandeuphonie/raw/master/public/combined.png "Example 1")

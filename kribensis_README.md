# Kribensis - A Python Dropbox Client

I love Dropbox.  Ideally there would be a Dropbox client for Raspberry Pi so easy cross-machine file syncronization would be as automatic for Raspberry Pi as it is for Mac, PC, and Linux systems.  Alas, as of this writing there isn\'t one.  However, there is a Dropbox SDK for Python.  I therefore decided to write a simple utility that could get/put files between my Raspberry Pi and my Dropbox account.

## Usage 

Usage is simple.  The -put option lets you transfer a local file to Dropbox:

```
kribensis.py -put local_file remote_file
```

The -get option lets you retriev a file from Dropbox:

```
kribensis.py -get remote_file local_file
```

For security reasons, applications registered with Dropbox are assigned a special folder in the Dropbox/Apps subfolder.  This means files transferred to Dropbox by kribensis will be found in the Dropbox/Apps/kribensis folder.  Files to be downloaded must be in the folder before being retrieved.

### Authorization

The first time you use kribensis you will need to authorize it to access your Dropbox account.  You do this with the -a or --authorize options (both are equivalent). Kribensis will generate a unique Dropbox access token which it will present to you as a URL. Simple copy and paste that URL into your browser and follow the instructions.  Once authorized kribensis stores authorization information in a file in your home directory so it won\'t need to be authorized every time you use it.

## So What\'s With The Name?

Any application accessing Dropbox must be registered, and registered application names must be unique.  I wasted nearly an hour proposing names for my application and every one of them was taken.  Exasperated, I decided to try names of tropical fish and the first one I tried was \'kribensis\', an [African cichlid](http://en.wikipedia.org/wiki/Pelvicachromis_pulcher) I successfully raised while a college student.  Happily that name wasn\'t taken.


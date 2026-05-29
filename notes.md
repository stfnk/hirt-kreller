
## New Project Pages
Duplicate one of the existing html pages in `workfiles/projects/` each project_name.html should have a corresponding project_name/ directory where all related media files are located. Create that if it does not exist yet. 
The folder should contain a header image file that is used as the project page header image. Remaining images and videos can be arranged on the page using the same mechanics as on all other pages.

## Publishing
The page is mostly static html files, except the blog. Blog entries are automatically generated from a prototype page and also injected into the index page's blog area - where the header images of multiple entries appear in a slideshow.

Run `publish.py` python script to convert blog entries from custom markdown to proper html using `blog/entry_prototype.html`. For now this script performs various steps to move all relevant files from workfiles to publish folder. 
Additionally to generating blog entry html pages and connecting Prev + Next buttons it also injects and links entries into the showcase panel on the main page.

## Bugs
- [ ] profile pages scale weird with narrow pages
- [ ] vertical (portrait) images in galleries are cropped weirdly

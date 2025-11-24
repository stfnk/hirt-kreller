import os
import shutil
from sysconfig import get_preferred_scheme

# collected data for blog entries
titles = []
headers = [] # paths to header images
dates = []
contents = []

src_dir = "workfiles/"
blog_src_dir = "workfiles/blog/"
publish_dir = "publish/"

static_files = [
    "index.html",
    "luna_hirt.html",
    "stefan_kreller.html",
    "style.css",
    "about.css",
    "showcase.css",
    "showcase.js",
    "blog/blog.css",
]

static_directories = [
    "content",
    "blog/content",
]

def extract_blog_data(html_file):
    # open file and collect content
    with open(html_file, "r") as file:
        file_content = file.read()

    date = file_content.split("_DATE_")[1]
    title = file_content.split("_TITLE_")[1]
    header = file_content.split("_HEADER_")[1]
    content = file_content.split("_CONTENT_")[1]

    dates.append(date)
    headers.append(header)
    titles.append(title)
    contents.append(content)


def collect_blog_entries():
    # scan folder for written entries & parse necessary information from them
    for dirpath, dirnames, filenames in os.walk(blog_src_dir):
        for file in filenames:
            if file == "blog.css":
                break
            if file == "entry_prototype.html":
                break

            extract_blog_data(os.path.join(dirpath, file))
        break

    # reverse order to have newest first
    dates.reverse()
    headers.reverse()
    titles.reverse()
    contents.reverse()
    print("reversed data lists")


def blog_entry_name(date):
    # construct entry's name from date
    tokens = date.split(".")
    assert len(tokens) == 3
    return tokens[2] + tokens[1] + tokens[0]

def construct_local_blog_url(index: int):
    name = blog_entry_name(dates[index])
    return name + ".html"

def get_next_blog_entry(current: int) -> str:
    if (current <= 0):
        return ""

    return construct_local_blog_url(current-1)

def get_prev_blog_entry(current: int) -> str:
    if (current >= len(titles)-1):
        return ""

    return construct_local_blog_url(current+1)

def prepare_blog_entry(index: int) -> str:
    # create a new prototype page content
    prototype_path = blog_src_dir + "entry_prototype.html"

    with open(prototype_path, "r") as file:
        file_content = file.read()

    # replace placeholder in html prototype
    file_content = file_content.replace("_TITLE_", titles[index])
    file_content = file_content.replace("_DATE_", dates[index])
    file_content = file_content.replace("_CONTENT_", contents[index])
    file_content = file_content.replace("_HEADER_IMAGE_", headers[index])

    next_url = get_next_blog_entry(index)
    if next_url == "":
        file_content = file_content.replace("_NEXT_STYLE_", "display: none;")
    else:
        file_content = file_content.replace("_NEXT_ENTRY_URL_", next_url)

    prev_url = get_prev_blog_entry(index)
    if prev_url == "":
        file_content = file_content.replace("_PREV_STYLE_", "display: none;")
    else:
        file_content = file_content.replace("_PREV_ENTRY_URL_", prev_url)

    return file_content


def write_blog_entry(entry_html: str, date):
    entry_file = publish_dir + "blog/" + blog_entry_name(date) + ".html"
    with open(entry_file, "w") as entry:
        entry.write(entry_html)

    print("created: " + entry_file)


def publish_blog_entries():
    for i in range(len(titles)):
        write_blog_entry(prepare_blog_entry(i), dates[i])

    prepare_index_showcase()


def create_index_showcase_entry(index_html: str, index: int) -> str:
    # creates a single showcase entry, from prototype defined in index_html
    # extract showcase entry prototype from html
    prototype = index_html.split("<!-- _SHOWCASE_ENTRY_PROTOTYPE_ -->")[1]

    # replace prototype data
    prototype = prototype.replace("_TITLE_", titles[index])
    prototype = prototype.replace("_DATE_", dates[index])
    prototype = prototype.replace("_TEXT_", "")  # TODO
    prototype = prototype.replace("_HEADER_IMG_", "blog/" + headers[index])
    prototype = prototype.replace(
        "_BLOG_URL_", "blog/" + blog_entry_name(dates[index]) + ".html"
    )

    # TODO: remove need to change id
    prototype = prototype.replace("current_entry", "entry" + str(index))

    return prototype


def prepare_index_showcase():
    published_index_file = os.path.join(publish_dir, "index.html")

    # laod index html text
    with open(published_index_file, "r") as file:
        index_html = file.read()

    entries = []

    for i in range(len(titles)):
        entry = create_index_showcase_entry(index_html, i)
        entries.append(entry)

    entries.reverse()

    # write to the published index.html
    showcase_entries_html = ""
    for entry in entries:
        showcase_entries_html += entry + "\n"
        print("index.html: injected showcase entry")

    index_html = index_html.replace("<!-- ENTRY_STORAGE -->", showcase_entries_html)

    # write back to actual published index.html
    with open(published_index_file, "w") as entry:
        entry.write(index_html)


def copy(from_path, to_path):
    if os.path.exists(to_path):
        os.remove(to_path)
    shutil.copy2(from_path, to_path)


def copy_static_files():
    # copies (and replaces) static files in publish directory
    for path in static_files:
        from_path = os.path.join(src_dir, path)
        to_path = os.path.join(publish_dir, path)
        copy(from_path, to_path)
        print("published " + path)

    for dir in static_directories:
        shutil.copytree(os.path.join(src_dir, dir), os.path.join(publish_dir, dir))
        print("published " + dir + "/")


def wipe_publish():
    print("wipe publish...")
    if os.path.exists(publish_dir):
        shutil.rmtree(publish_dir)

    os.mkdir(publish_dir)
    os.mkdir(publish_dir + "/blog")


wipe_publish()
collect_blog_entries()
copy_static_files()
publish_blog_entries()

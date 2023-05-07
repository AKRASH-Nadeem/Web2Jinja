from bs4 import BeautifulSoup
import os
import shutil
import re
import urllib.parse

# Utility functions
def is_file_path(path):
    base, ext = os.path.splitext(path)
    return bool(ext)  # Returns True if the extension is non-empty, False otherwise


def check_path_type(path):
    if path.startswith("#"):
        return None
    elif path == "true" or path == "false":
        return None
    result = urllib.parse.urlparse(path)
    if result.scheme:
        return "online"
    elif re.match(r"^(\/|\w:)", path):
        return "absolute"
    elif re.match(r"^(?!\/)(?!([A-Za-z]:\\)).*", path):
        return "relative"
    else:
        return "no_path"



def make_valid_function(s):
    # Replace all non-alphanumeric characters with underscores
    s = re.sub(r'[^0-9a-zA-Z_]+', '_', s)

    # Remove any leading underscores
    s = re.sub(r'^_+', '', s)

    # If the string is empty or starts with a number, add an underscore at the beginning
    if not s:
        pass
    elif s[0].isdigit():
        s = '_' + s

    return s


# Change all href attributes accordingly
def href_changer(link):
    if 'href' in link.attrs:
        if link['href'].startswith('#'):
            return
        elif link['href'] == "/":
            link['href'] = """{{ url_for('index') }}"""
        elif link['href'].startswith("/") and link['href'].endswith(".html"):
            _na = link['href'].replace(".html","")
            name = make_valid_function(_na)
            link['href'] = """{{ url_for('"""+name+"""') }}"""
            print(link['href'])
            return
        elif check_path_type(link['href']) == "online":
            return
        elif link['href'].endswith(".html"):
            _na = link['href'].replace(".html","")
            name = make_valid_function(_na)
            link['href'] = """{{ url_for('"""+name+"""') }}"""
            print(link['href'])
            return
        link['href'] = "{{ url_for('static',filename='"+link['href']+"') }}"

# Change all src attributes accordingly
def src_changer(link):
    if 'src' in link.attrs:
        if link['src'].startswith('#'):
            return
        elif check_path_type(link['src']) == "online":
            return
        link['src'] = "{{ url_for('static',filename='"+link['src']+"') }}"

# Change other tags with attributes in body
def body_tag_changer(body_tag):
    ignoreable_attributes = ['class','id',"alt","for","type","placeholder","target"]
    for tag in body_tag.find_all():
        for attr in tag.attrs:
            if attr == "href":
                href_changer(tag)
            elif attr == "src":
                src_changer(tag)
            elif attr in ignoreable_attributes:
                pass
            else:
                path = tag[attr]
                result = check_path_type(path)
                if result != "online" and result != "no_path" and result != None:
                    if is_file_path(path):
                        tag[attr] = """{{ url_for('static',filename='""" + path + """') }}"""
                        print(attr," : ",tag[attr])
                    
                else:
                    pass
    return body_tag


# change all hrefs and src using by just passing soup object
def change_every_linkable_tag(soup,folder,static_folder):
    hrefs = soup.find_all(href=True)
    if len(hrefs) > 0:
        for link in hrefs:
            href_changer(link)
    srcs = soup.find_all(src=True)
    if len(srcs) > 0:
        for link in srcs:
            src_changer(link)
    

# Get all files in the folder copy assets and return set of html files
def copy_all_assets(root_directory,new_directory):
    # create the new directory if it doesn't exist
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    list_html_files = set()

    # loop through all directories and files in the root directory
    for root, dirs, files in os.walk(root_directory):

        # loop through all files in the current directory
        for file in files:
            # check if the file has a .html extension
            if not file.endswith('.html'):
                # create a corresponding directory in the new directory
                for_static_root = root.replace(root_directory, "static")
                new_root = os.path.join(new_directory,for_static_root)
                # print(new_root)
                if not os.path.exists(new_root):
                    os.makedirs(new_root)
                # copy the file to the corresponding directory in the new directory
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(new_root, file)
                shutil.copy2(old_file_path, new_file_path)
            elif file.endswith(".html"):
                # create a corresponding directory in the new directory
                for_template_root = root.replace(root_directory, "templates")
                new_root = os.path.join(new_directory,for_template_root)
                # print(new_root)
                if not os.path.exists(new_root):
                    os.makedirs(new_root)
                replaced_path = root.replace(root_directory,"")
                file_p = os.path.join(replaced_path,file).removeprefix("/") if os.path.join(replaced_path,file).startswith("/") else os.path.join(replaced_path,file)
                # print(file_p)
                list_html_files.add(file_p)
    return list_html_files
def navbar_(navbar):
    print("in navbar_".center(100,"-"))
    if navbar and len(navbar) > 0:
        navbar = navbar[0]
        fname = os.path.join(templates_folder,"navbar.html")
        print(fname)
        with open(fname,"w") as navf:
            change_every_linkable_tag(navbar,folder,static_folder)
            print("writing...")
            navf.write(navbar.prettify())
            navbar_element["element"] = {"tag":navbar_tag,"class":navbar_class if navbar_class and navbar_class != "" else None,"id":navbar_id if navbar_id and navbar_id != "" else None}
        navbar.extract()
        return True
    else:
        return False
# get the Folder path in which the files are
folder = input("folder > ")
navbar_tag = str(input("navegation bar tag name > "))
navbar_class = str(input("navegation bar class (leave empty if there is none) > "))
navbar_id = str(input("navegation bar id (leave empty if there is none) > "))

# check if folder exists
if os.path.exists(folder):
    navbar_element  = {}
    # foldername to save the changes
    folder_name = folder + "_flask"
    # print(folder)
    # copy all assets and get files
    html_files = copy_all_assets(folder,folder_name)
    # Create required folders
    try:
        static_folder = os.path.join(folder_name,'static')
        templates_folder = os.path.join(folder_name,'templates')
        if not os.path.exists(templates_folder):
            os.mkdir(templates_folder)
    except FileExistsError as error:
        print("[_] " + error.filename + " already exists")
    except Exception as error:
        print(error)
    # Get header tags in a dictionary with file name as the key
    headers_tags_dictionary = {}
    # Get script tags in a dictionary with file name as the key
    script_tags_in_body_dictionary = {}
    # Loop over all the html files
    got_navbar = False
    for fil in html_files:
        path = os.path.join(folder,fil)
        # print(path)
        read_file = open(path,"r")
        soup = BeautifulSoup(read_file,'html.parser')
        read_file.close()
        header = soup.find("head")
        if header:
            header_tags = header.find_all()
        body = soup.find("body")
        if not got_navbar:
            print("getting navbar".center(100,"-"))
            # find navbar
            if navbar_tag != None and navbar_tag != "":
                if navbar_class != None and navbar_class != "" and navbar_id != None and navbar_id != "":
                    navbar = soup.find_all(navbar_tag,{"class":navbar_class,"id":navbar_id})
                elif navbar_id != None and navbar_id != "":
                    # print(navbar_tag,navbar_id)
                    navbar = soup.find_all(navbar_tag,{"id":navbar_id})
                elif navbar_class != None and navbar_class != "":
                    navbar = soup.find_all(navbar_tag,{"id":navbar_class})
                else:
                    navbar = soup.find_all(navbar_tag)
                print(navbar)
                if navbar and len(navbar) > 0:
                    # use navbar function
                    nav_result = navbar_(navbar)
                    if nav_result:
                        got_navbar = True
            else:
                pass
            print("".center(100,"-"))
        body_script_tags = body.find_all("script")
        if header:
            headers_tags_dictionary[str(fil)] = header_tags
        if body_script_tags:
            print("body_script_tags".center(100,'-'))
            print(body_script_tags)
            print("".center(100,'-'))
            script_tags_in_body_dictionary[str(fil)] = body_script_tags
    # target main index.html file to compare the links and scripts and find same tags
    main_page = input("name of home page (index.html or home.html) > ")
    # Get same header tags in all files
    same_header_tags_sets = [headers_tags_dictionary[i] for i in headers_tags_dictionary.keys()]
    same_header_tags = headers_tags_dictionary[main_page]
    for s in same_header_tags_sets:
        same_header_tags = [xt for xt in same_header_tags if xt in s]
    # Get same script tags in all files
    same_script_tags_sets = [script_tags_in_body_dictionary[i] for i in script_tags_in_body_dictionary.keys()]
    same_script_tags = script_tags_in_body_dictionary[main_page]
    for s in same_script_tags_sets:
        same_script_tags = [xt for xt in same_script_tags if xt in s]
    print(same_script_tags)
    # read index.html file 
    main_file_path = os.path.join(folder,main_page)
    read_file = open(main_file_path,'r')
    soup = BeautifulSoup(read_file,"html.parser")
    read_file.close()
    header = soup.find("head")
    body = soup.find("body")
    # remove all tags in header and body tag
    header.clear()
    body.clear()
    # add title tag
    title_tag = soup.new_tag("title")
    title_tag.string = "{% block title %}{% endblock title %}"
    # append title tag
    header.append(title_tag)
    # add list of header tags that are same in every html file
    header.contents.extend(same_header_tags)
    header.append("""{% block head %}{% endblock head %}""")
    if nav_result:
        body.append("""{% include 'navbar.html' %}""")
    body.append("""{% block content %}{% endblock content %}""")
    # add list script of tags that are same in every html file
    body.contents.extend(same_script_tags)
    body.append("""{% block script %}{% endblock script %}""")
    # print(soup.prettify())
    base_html = soup.prettify()
    soup = BeautifulSoup(base_html,"html.parser")
    # Change every tag according to flask template
    change_every_linkable_tag(soup,folder,static_folder)
    # print(soup.prettify())
    base_html = soup.prettify()
    # Write base.html file
    with open(os.path.join(templates_folder,"base.html"),'w') as f:
        f.write(base_html)
    # loop over all html files and inherit base.html
    base_extent = "{% extends 'base.html' %}\n"
    for fil in html_files:
        path = os.path.join(folder,fil)
        read_file = open(path,"r")
        soup = BeautifulSoup(read_file,'html.parser')
        read_file.close()
        # remove navbar from the page
        if len(navbar_element) > 0:
            print("navbar_removing".center(100,"0"))
            print(navbar_element["element"]['tag'],navbar_element["element"]["class"],navbar_element["element"]["id"])
            if navbar_element["element"]["class"] and navbar_element["element"]["id"]:
                to_remove = soup.find(navbar_element["element"]['tag'],{"class":navbar_element["element"]["class"],"id":navbar_element["element"]["id"]})
            elif navbar_element["element"]["class"]:
                to_remove = soup.find(navbar_element["element"]['tag'],{"class":navbar_element["element"]["class"]})
            elif navbar_element["element"]["id"]:
                to_remove = soup.find(navbar_element["element"]['tag'],{"id":navbar_element["element"]["id"]})
            else:
                to_remove = soup.find(navbar_element["element"]['tag'])
            if to_remove:
                print(to_remove)
                print("removing_navbar".center(100,"-"))
                to_remove.extract()
        header = soup.find("head")
        header_tags = header.find_all()
        body = soup.find("body")
        body_script_tags = body.find_all("script")
        unique_headers_tags = [x for x in header_tags if x not in same_header_tags]
        unique_script_tags = [x for x in body_script_tags if x not in same_script_tags]

        title_block = ""
        header_block = "{% block head %}\n"
        for header_tag in unique_headers_tags:
            if header_tag.name == 'title':
                title_block = "{% block title %}"
                title_block += header_tag.text
                title_block += "{% endblock title %}\n"
            else:
                # print(header_tag)
                href_changer(header_tag)

                header_block += header_tag.prettify()
        header_block += "\n{% endblock head %}\n"
        header_content = title_block + header_block

        for script_tag in body.find_all("script"):
            script_tag.extract()

        script_block = "\n{% block script %}\n"
        for script_tag in unique_script_tags:
            src_changer(script_tag)
            script_block += script_tag.prettify()
        script_block += "\n{% endblock script %}\n"
        body_block = "{% block content %}\n"
        inner_html = ''.join(str(elem) for elem in body.contents)
        body_soup = BeautifulSoup(inner_html,"html.parser")

        body_soup = body_tag_changer(body)
        
        body_block += body_soup.prettify()
        body_block += "\n{% endblock content %}"
        page_content = base_extent + header_content + body_block + script_block

        # print(page_content)
        print(fil.center(100,'-'))
        with open(os.path.join(templates_folder,fil),'w') as fl:
            fl.write(page_content)
    python_main_file = os.path.join(folder_name,'main.py')
    main_content = """from flask import Flask,render_template\n\napp = Flask(__name__)\n\n"""
    for fil in html_files:
        _name = fil.replace(".html", "")
        function_name = make_valid_function(_name)
        if fil == main_page:
            route = "/" + function_name
            main_content += f"""@app.route('/')\n@app.route('{route}')\ndef {function_name}():\n\treturn render_template('{fil}')\n\n"""
        else:
            route = "/" + function_name
            main_content += f"""@app.route('{route}')\ndef {function_name}():\n\treturn render_template('{fil}')\n\n"""
    main_content += """\nif __name__ == '__main__':\n\tapp.run(debug=True)"""
    with open(python_main_file,"w") as f:
        f.write(main_content)
else:
    print("No folder name \"",folder,"\" Found")

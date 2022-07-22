from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

URL = ""
FKW = ""

def user_input():
    global URL, FKW
    URL = input("Enter url: ")
    FKW = input("Enter Focus Keyword: ")

def extract(url):
    req = requests.get(url, headers={"User-Agent": "XY"})
    res = req.status_code
    if res >= 200 and res <300:
        return BeautifulSoup(req.text, "html.parser")
    else:
        return res


def remove_HF(D):
    """This function will remove
    header and footer from body"""
    newD = D
    remove = ["header", "footer"]
    try:
        for tags in remove:
            newD.find(tags).decompose()
    except AttributeError:
        newD.find(remove[1]).decompose()
    except Exception as e:
        print("Error Occured :", e)
        newD = D
    return newD

def isFKWpresent(kw, content, is_iterator = False):
        """this function will check if Focus Keyword
        is present in particular content or not"""
        kws = []
        number_of_fkw = 0
        try:
            if is_iterator == False:
                for i in kw.split(" "):
                    if i.lower() in content.lower().split(" "):
                        kws.append(i)
                        number_of_fkw += 1
                    else:
                        pass
            else:
                for i in kw.split(" "):
                    for c in content:
                        if i.lower() in c.lower():
                            kws.append(i)
                            number_of_fkw += 1
                        else:
                            pass
            if kws == []:
                return False, "Focus Keyword Not Found"
            else:
                fkws = []
                dummy = [fkws.append(i) for i in kws if i not in fkws]
                fkws_as_astring = ", ".join(i for i in fkws)
                return True, fkws_as_astring
            
        except Exception as e:
            print("FKW Exception", e)
            return None, "Not Found"


Y = "√"
N = "><"

class Meta_data:
    def __init__(self, data):
        self.D = data
    
    meta_info = {"Title": "", "Title Length": 0, "Description" : "", "Description Length":0, 
                "Canonical Url": "", "Viewport": "", "Robots": "", "Author": ""}
    
    def get_title(self):
        try:
            title = self.D.title.text
            if title:
                self.meta_info["Title"] = title
                return True, title
        except TypeError:
            return False, "Meta Title Not Found"
    
    def is_FKW_in_title(self):
        title = self.get_title()
        is_present = isFKWpresent(FKW, title[1])
        if is_present[0] == True:
            return f"{Y} Focus Keywords in Title: {is_present[1]}"
        elif is_present[0] == False:
            return f"{N} Focus Keyword missing in Title"
        else:
            return "Not Found"

    def get_description(self):
        """Extract Description"""
        try:
            desc = self.D.find("meta", {"name" : "description"}).get("content")
            if desc:
                self.meta_info["Description"] = desc
                return True, desc
            else:
                return True, self.D.find("meta", property = "og:description").get("content")
        except:
            return "Meta Description Not Found"
    
    def is_FKW_in_description(self):
        desc = self.get_description()
        is_present = isFKWpresent(FKW, desc[1])
        if is_present[0] == True:
            return f"{Y} Focus Keyword is in meta description: {is_present[1]}"
        elif is_present[0] == False:
            return f"Focus Keyword missing in meta description"
        else:
            return None, "Not Found"
    
    
    url_length = 0
    
    def is_url_length_valid(self):
        if self.url_length == 0:
            return None, "Not Found"
        elif self.url_length < 85 :
            return f"{Y} Length of url is: {self.url_length}. Which is not bad"
        elif self.url_length >= 85:
            return f"{N} Length of url is: {self.url_length} reduce if you can"
    
    def parse_url(self):
        """remove /.-=_ from url and return 
        text from url as a string"""
        res = URL
        remove = "/.-=_"
        for i in remove:
            res = res.replace(i, " ")
        return res
    
    def is_FKW_in_url(self):
        "This will check if FKW is present in url"
        parsed_url = self.parse_url() #Parse Url
        is_present = isFKWpresent(FKW, parsed_url)
        result = is_present[0] # Storing result
        if result == False: 
            kw_without_spaces = FKW.replace(" ", "").lower()
            if kw_without_spaces in parsed_url: # Checking if fkw is presnt by clearing spaces
                result = True # Updating result if FKW found
                return f"{Y} FKW is defined in url"
            else:
                return f"{N} Focus Keyword Not found in url"
        elif result == True:
            return f"{Y} FKW is defined in url."
        else:
            return "Not Found"
    
    title_length = 0
    def is_title_length_valid(self):
        if self.title_length == 0:
            return "Not Found"
        elif self.title_length < 65:
            return f"{Y} Length of Title is: {self.title_length} which is not bad"
        else:
            return f"{N} Length of Title is: {self.title_length}. The ideal length is between 30-65 charecters"
            
    description_length = 0

    def is_desc_length_valid(self):
        if self.description_length == 0:
            return "Not Found"
        elif self.description_length >= 60 and self.description_length <= 165:
            return f"{Y} The Length of decription is: {self.description_length}"
        elif self.description_length <60 or self.description_length >165:
            return f"{N} Length of description is: {self.description_length}"

    def update_length(self):
        """
        This function will update the length of url,
        title, description and based on its length it
        will update if the length is valid or not
        """
        try:
            self.url_length = len(URL)
        except TypeError:
            pass
        try:
            TL = self.get_title()
            self.title_length = len(TL[1])
            self.meta_info["Title Length"] = self.title_length
        except TypeError:
            pass
        try:
            DL = self.get_description()
            self.description_length = len(DL[1])
            self.meta_info["Description"] = len(DL[1])
        except TypeError:
            pass
    
    def canonical_url(self):
        """Check canonical tag"""
        try:
            canonical_url = self.D.head.find("link", {"rel":"canonical"})["href"]
            if canonical_url:
                if canonical_url == URL:
                    self.meta_info["Canonical Url"] = canonical_url
                    return f"{Y} Good Canonical url is defined and is same as webpage url"
                else:
                    self.meta_info["Canonical Url"] = canonical_url
                    return f"{N} Canonical url is defined but is not same as webpage url"
            else:
                return "Canonical Tag Not found"
        except TypeError:
            return "Not found"

    def viewport(self):
        """Check mobile viewport"""
        viewport = self.D.find("meta", {"name":"viewport"}).get("content")
        if viewport:
            self.meta_info["Viewport"] = viewport
            return f"{Y} viewport meta tag is defined"
        else:
            self.meta_info["Viewport"] = viewport
            return f"{N} viewport meta tag is missing"
        
    def is_page_indexable(self):
        try:
            robot = self.D.find("meta", {"name":"robots"}).get("content")
            if robot:
                for i in robot.split(","):
                    if i == "noindex":
                        self.meta_info["Robots"] = robot
                        return f"{N} Page cannot be indexed"
                    else:
                        self.meta_info["Robots"] = robot
                        return f"{Y} Page can be indexed by search engine bots"
            else:
                pass
        except Exception as e:
            print(e)
            pass
    
    
    
class Textdata:
    """Text"""
    def __init__(self, data):
        self.D = data
    
    text_info = {}
    
    def page_text(self):
        try:
            text = self.D.body.findAll(text=True)
            skip_tags = ['style', 'noscript', 'aside' 'body', 'html', 'a', 'figure',
                 'input', 'script', 'head', 'title', 'meta', '[document]', 'div', 'option', 'article',
                'form', 'footer', 'link', 'section', 'nav', 'img', 'body', 'button']
            result = [i for i in text if not i.parent.name in skip_tags and not i == "\n" and not i == " "]
            if not result == []:
                return result
            else:
                return "Page text not found"
        except Exception:
            pass
        
    
    def code_to_text_ratio(self):
        page_text_content = self.page_text()
        code = str(self.D)
        text = " ".join(page_text_content)
        c = len(code)
        t = len(text)
        precentage = (t/c)*100 
        return f"Total letters of code: {c}\nTotal letters of text: {t}\nText to Code Percentage: {precentage:.2f}%"
    
    def kw_density(self):
        pass

    def get_first_sentence(self):
        try:
            first_sentence = self.D.body.find("p").text
            if first_sentence != None and first_sentence != "":
                return True, first_sentence
            else:
                return None, "Cannot find first sentence."
        except TypeError:
            return False
        except Exception as e:
            return None
    
    def is_FKW_in_first_sentence(self):
        first_sentence =  self.get_first_sentence()
        if first_sentence[0] == True:
            is_present = isFKWpresent(FKW, first_sentence[1])
            if is_present[0] == True:
                return f"{Y} Focus Keyword ({is_present[1]}) is present in the first sentence(<p> tag)"
            elif is_present[0] == False:
                return f"{N} Focus keyword missing in first sentence(<p> tag)"
        else:
            return f"{Y} Cannot find first sentence."
        
    def is_FKW_in_the_initial(self):
        try:
            page_text_content = self.page_text()
            initial_content = " ".join(page_text_content).split(" ")[:500]
            if initial_content:
                is_present = isFKWpresent(FKW, initial_content, is_iterator=True)
                if is_present[0] == True:
                    return f"{Y} Focus keyword {is_present[1]} is preset in the first 500 words of the webpage"
                elif is_present[0] == False:
                    return f"{N} Focus keyword is missing in the first 500 words of the webpage"
            else:
                pass
        except Exception:
            pass

    def get_bold_text(self):
        try:
            b = []
            for i in self.D.body.findAll("strong"):
                b.append(i.text)
            if b != []:
                return True, b
            else:
                return None, "No bold text"
        except Exception:
            return False, "Bold text not found"
    
    def is_FKW_in_bold_text(self):
        bold_text = self.get_bold_text()
        if bold_text[0] == True:
            is_presnt = isFKWpresent(FKW, bold_text[1], is_iterator=True)
            if is_presnt[0] == True:
                return f"{Y} Focus Keyword in bold text"
            elif is_presnt[0] == False:
                return f"{N} Focus keyword not in the bold text"
        else:
            return "Bold text not found"        
    
    """----Headings----"""
    
    Headings = {"h1":[], "h2":[], "h3":[], "h4":[], "h5":[], "h6":[]}
    h_order = []
    total_headings = 0

    def update_headings(self):
        tag_count = 1
        while tag_count < 7:
            H = "h"+str(tag_count)
            h_tags = self.D.findAll(H)
            for tags in h_tags:
                self.total_headings += 1
                self.Headings[H].append(tags.text.replace("\n", "").strip())
                self.h_order.append(tag_count)
            tag_count+=1
    
    def is_htags_in_right_format(self):
        if self.h_order == []:
            return "h tags not found"
        elif len(self.h_order) < 2:
            return "Only 1 heading tag found"
        else:
            H = [0]
            for i in self.h_order:
                H.append(i)
                if H[-2] > i:
                    return f"{N} h tags are not in hierarchy of h1-h6"
                else:
                    pass
            return f"{Y} h tags are in hierarchy of h1-h6"
    
    def is_single_h1(self):
        h1 = self.Headings["h1"]
        num_of_h1 = len(h1)
        if num_of_h1 == 1:
            return f"{Y} Only 1 h1 tag"
        elif num_of_h1 > 1:
            return f"{N} There are {len(h1)} h1 tags found"
        else:
            return f"{N} h1 not found"
        
    def get_h1(self):
        try:
            h1 = self.D.body.find("h1").text
            return True, h1
        except Exception:
            return False, "h1 not found"
        
    def is_FKW_in_h1(self):
        is_h1_found = self.get_h1()
        if is_h1_found[0] == True:
            h1 = is_h1_found[1]
            is_present = isFKWpresent(FKW, h1)
            if is_present[0] == True:
                return f"{Y} Focus Keyword ({is_present[1]}) is present in the h1 tag"
            elif is_present[0] == False:
                return f"{N} Try to add Focus keyword in the h1 tag"
        else:
            return "h1 tag not found"

class Images:

    def __init__(self, data):
        self.D = data
    
    img_info = {"total images":0, "with alt count":0, "with alt links":[], "alt attributes":[],
    "without alt count":0, "without alt links":[]}

    def update_images_info(self):
        try:
            for i in self.D.body.find_all("img"):
                self.img_info["total images"] +=1
                alt = i["alt"]
                if alt != "" and alt != None:
                    self.img_info["with alt count"] += 1
                    self.img_info["with alt links"].append(i["src"])
                    self.img_info["alt attributes"].append(alt)
                else:
                    self.img_info["without alt count"] += 1
                    self.img_info["without alt links"].append(i["src"])
        except Exception as e:
            return e
    
    def clear_img_info(self):
        self.img_info.clear()


class Links:

    def __init__(self, data):
        self.D = data
    
    links_info = {"total links":0, "internal count":0, "internal links":[],
              "external count":0, "external links":[], "dofollow count":0, "dofollow":[],
              "nofollow count":0, "nofollow":[], "na links count":0, "na links":[]}

    def get_links_info(self):
        domain = urlparse(URL).netloc
        D_name_with_ext = domain
        if "www." in D_name_with_ext:
            D_name_with_ext = D_name_with_ext.replace("www.", "")
        for li in self.D.body.find_all("a"):
            link = li.get("href")
            link_domain = urlparse(link).netloc
            if type(link) == str:
                if not link.startswith(("tel:", "#", "mailto:", "javascript:")):

                    # Internal External Links
                    self.links_info['total links'] += 1
                    
                    if link_domain == domain or link.startswith("/") or link_domain.endswith(D_name_with_ext): #Internal links
                        self.links_info["internal count"] +=1
                        self.links_info["internal links"].append(link)
                    else: # External links
                        self.links_info['external count'] += 1
                        self.links_info['external links'].append(link)

                    # Dofollow nofollow links
                    rel_attribute = li.get('rel')
                    if rel_attribute != None:
                        if "nofollow" in rel_attribute:
                            self.links_info['nofollow count'] += 1
                            self.links_info['nofollow'].append(link)
                        else:
                            self.links_info['dofollow count'] += 1
                            self.links_info['dofollow'].append(link)
                    else:
                        self.links_info['dofollow count'] += 1
                        self.links_info['dofollow'].append(link)

                else:
                    self.links_info['na links count'] += 1
                    self.links_info['na links'].append(link)
                    
            else:
                #print("Invalid link: ", li)
                pass

    def check_nofollow_internal_links(self):
        nofollow_links = self.links_info['nofollow']
        if nofollow_links != []:
            for links in nofollow_links:
                pass

    def clear_links_info(self):
        self.links_info.clear()
    
        
def line_break(width):
    print(width*"-")

def on_page_seo_report():
    #Update FKW and Url
    user_input()
    
    print("Processing...")
    #Extract data
    data = extract(URL)
    
    #Check is page srcapable
    if type(data) == int:
        print("Cannot extract webpage data with response code: ", data)
        from time import sleep
        sleep(2)
        
    else:
        #Remove header and footer
        data_x = remove_HF(data)

        """__________Meta Data__________"""
        meta = Meta_data(data)
        print(40*"_"+"META"+"_"*40)
        
        #Robots tag
        indexable = meta.is_page_indexable()
        if not indexable == None:
          print("Robots: ", indexable)
          line_break(40)
        else:
          pass

        #Title
        title = meta.get_title()
        meta.update_length()
        is_t_len_valid = meta.is_title_length_valid()
        fkw_in_t = meta.is_FKW_in_title()

        print("Title: ", title)
        line_break(20)
        print("Title length: ", is_t_len_valid)
        line_break(20)
        print("Fkw in Title: ", fkw_in_t)

        line_break(40)

        #Description
        desc = meta.get_description()
        is_d_len_valid = meta.is_desc_length_valid()
        fkw_in_d = meta.is_FKW_in_description()

        print("Description: ", desc)
        line_break(20)
        print("Description length: ", is_d_len_valid)
        line_break(20)
        print("Fkw in Description: ", fkw_in_d)

        line_break(40)

        #Url
        url_len = meta.is_url_length_valid()
        fkw_in_url = meta.is_FKW_in_url()

        print("Url Length: ", url_len)
        line_break(20)
        print("FKW in Url: ", fkw_in_url)

        line_break(40)

        #Other meta
        canonical = meta.canonical_url()
        viewport = meta.viewport()

        print("Canonical Url: ", canonical)
        line_break(20)
        print("Viewport: ", viewport)



        """__________Text Data__________"""
        print(40*"_"+"TEXT"+"_"*40)

        text = Textdata(data_x)
        #text.get_first_sentence()
        fkw_in_first_sentence = text.is_FKW_in_first_sentence()
        fkw_in_initial_content = text.is_FKW_in_the_initial()
        #bold_text = text.get_bold_text()
        fkw_in_bold = text.is_FKW_in_bold_text()
        text.update_headings()
        headings = text.Headings
        heading_count = text.total_headings
        h1_h6_format = text.is_htags_in_right_format()
        h1_count = text.is_single_h1()
        fkw_in_h1 = text.is_FKW_in_h1()
        code_to_text_ratio = text.code_to_text_ratio()

        print("FKW in first p tag: ", fkw_in_first_sentence)
        line_break(20)
        print("FKW in inital content: ", fkw_in_initial_content)
        line_break(20)
        print("FKW in bold text: ", fkw_in_bold)
        line_break(20)
        print("Number of Headings: ", heading_count)
        line_break(20)
        #print("headings format: ", h1_h6_format)
        #line_break(20)
        print("Number of h1: ", h1_count)
        line_break(20)
        print("FKW in h1: ", fkw_in_h1)
        line_break(20)
        print("Code to Text Ratio: ", code_to_text_ratio)

        """__________Images__________"""
        print(40*"_"+"IMAGES"+"_"*40)
        img = Images(data_x)
        img.update_images_info()
        images = img.img_info
        img_count = images["total images"]
        with_alt = images["with alt count"]
        without_alt = images["without alt count"]

        print("Total Images: ", img_count)
        line_break(20)
        print("Images with alt: ", with_alt)
        view_alt_tags = input("Do you want to view alt attributes? (yes/no): ")
        if view_alt_tags == "n" or view_alt_tags == "no":
            pass
        else:
            for i in images["alt attributes"]:
                print(i)

        line_break(20)
        print("Images without alt: ", without_alt)
        view_images_without_alt = input("Do you want to view image links without alt? (yes/no): ")
        if view_images_without_alt == "n" or view_images_without_alt == "no":
            pass
        else:
            for i in images["without alt links"]:
                print(i)
                
        img.clear_img_info()
        """__________Links__________"""
        print(40*"_"+"LINKS"+"_"*40)
        links = Links(data_x)
        links.get_links_info()
        li = links.links_info
        total_links = li["total links"]
        internal = li["internal count"]
        external = li["external count"]
        dofollow = li["dofollow count"]
        nofollow = li["nofollow count"]

        print("Total Links: ", total_links)
        line_break(20)
        print("Total internal links: ", internal)
        line_break(20)
        view_internal = input("Do you want to see internal links?(yes/no): ")
        if view_internal == "n" or view_internal == "no":
            pass
        else:
            for i in li["internal links"]:
                print(i)
        line_break(20)
        print("Total External links: ", external)
        line_break(20)
        view_external = input("Do you want to see External links?(yes/no): ")
        if view_external == "n" or view_external == "no":
            pass
        else:
            for i in li["external links"]:
                print(i)
        print("Nofollow links: ", nofollow)
        line_break(20)
        print("Dofollow links: ", dofollow)
        links.clear_links_info()

on_page_seo_report()

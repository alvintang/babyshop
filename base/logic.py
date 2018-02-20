import re
import regex
import urllib.parse
import urllib.request, io
from PIL import Image

def getImageList(soup, img_list, source):
  # First get the meta description tag
  meta_image = soup.findAll('meta', attrs={'name':'og:image'}) or soup.findAll('meta', attrs={'property':'og:image'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_image:
    for meta in meta_image:
      print(meta.get('content'))
      img_list.append(meta.get('content'))
  else:
    print("None")

    for img in soup.find_all('img'):
        width = int(img.get('width',0))
        height = int(img.get('height',0))
        if(width > 150 and height > 150):
          if img.get('src').strip('/') not in img_list:
            #img_url = urllib.parse.quote(img.get('src').strip('/'))
            img_url = img.get('src').strip('/')
            print(img_url)
            img_list.append(img_url)

    if(len(img_list) > 0):
      print(img_list)
      return img_list

    imgs = re.findall(r'(https?:/)?(/?[\w_\-&%?./]*?)\.(jpg|png|gif)', source, re.M)

    for img in imgs:
      print(img)
      remote =  img[0] + img[1] + '.' + img[2]

      if(remote.startswith('http')):
        #img_file = io.BytesIO(urllib.request.urlopen(remote).read())
        #im=Image.open(img_file)
        #width, height = im.size
        if remote not in img_list:
          img_list.append(remote)

  return img_list

def getTitle(soup):
  # find title
  meta_title = soup.find('meta', attrs={'name':'og:title'}) or soup.find('meta', attrs={'property':'og:title'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_title:
    print("meta_title");
    return meta_title.get('content')
  else:
    return soup.title.get_text()
    #return soup.find('title').get('content')

def getPrice(soup, url):
  # find title
  meta_price = soup.find('meta', attrs={'name':'og:price:amount'}) or soup.find('meta', attrs={'property':'og:price:amount'}) or soup.find('meta', attrs={'name':'og:product:price:amount'}) or soup.find('meta', attrs={'property':'og:product:price:amount'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_price:
    return meta_price.get('content')
  elif url == 'https://babiestotoddlers.com/':
    print('babiesandtoddlers')
    price = soup.find('p', attrs={'class':'price large'})
    print(price.contents[0].contents)
    price_raw = re.sub(r'[^\x00-\x7f]',r'', price.contents[0].contents[0].replace(',',''))
    if price:
      return price_raw
  elif url == 'https://babymama.ph/':
    print('babymama')
    price = soup.find('span', attrs={'class':'woocommerce-Price-amount amount'})
    print(price.contents)
    if price:
      return price.contents[1].replace(',','')
  elif url == 'http://www2.hm.com/':
    print('h&m')
    price = soup.find('span', attrs={'class':'price-value'})
    price_str = price.contents[0].replace(',','').strip()
    price_str = price_str.replace('PHP ','')
    print(price_str)
    if price:
      return price_str
  else:
    res = regex.findall(r'(\p{Sc}|Php|PhP|php|PHP|&#8369;)\s?((?:\d+,)?\d+\.\d+)', soup.body.get_text())
    prices = []
    for r in res:
      prices.append(r[1])
    print(res)
    print(prices)
    if(len(prices) > 0):
      i = 0
      while(float(prices[i].replace(',','')) <= 0.00):
        i = i+1
      if(i > len(prices)):
        return ''
      return prices[i].replace(',','')
  return ''

def getCurrency(soup):
  # find title
  meta_currency = soup.find('meta', attrs={'name':'og:price:currency'}) or soup.find('meta', attrs={'property':'og:price:currency'}) or soup.find('meta', attrs={'name':'og:product:price:currency'}) or soup.find('meta', attrs={'property':'og:product:price:currency'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_currency:
    return meta_currency.get('content')
  else:
    return ''

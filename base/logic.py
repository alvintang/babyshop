import re

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

    imgs = re.findall(r'(https?:/)?(/?[\w_\-&%?./]*?)\.(jpg|png|gif)', source, re.M)

    for img in imgs:
      remote =  img[0] + img[1] + '.' + img[2]

      if(remote.startswith('http')):
        img_list.append(remote)

  return img_list

def getTitle(soup):
  # find title
  meta_title = soup.find('meta', attrs={'name':'og:title'}) or soup.find('meta', attrs={'property':'og:title'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_title:
    return meta_title.get('content')
  else:
    return ''

def getPrice(soup):
  # find title
  meta_price = soup.find('meta', attrs={'name':'og:price:amount'}) or soup.find('meta', attrs={'property':'og:price:amount'}) or soup.find('meta', attrs={'name':'og:product:price:amount'}) or soup.find('meta', attrs={'property':'og:product:price:amount'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_price:
    return meta_price.get('content')
  else:
    return ''

def getCurrency(soup):
  # find title
  meta_currency = soup.find('meta', attrs={'name':'og:price:currency'}) or soup.find('meta', attrs={'property':'og:price:currency'}) or soup.find('meta', attrs={'name':'og:product:price:currency'}) or soup.find('meta', attrs={'property':'og:product:price:currency'})

  # If description meta tag was found, then get the content attribute and save it to db entry
  if meta_currency:
    return meta_currency.get('content')
  else:
    return ''
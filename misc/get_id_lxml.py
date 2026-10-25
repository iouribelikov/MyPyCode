import lxml.html as html

e=html.fromstring(open("/Users/belikov/www/Astronomy/DeepSky/Galaxies/index.html").read()).get_element_by_id('M101')

attr=e[0].attrib
attr['href']='/path/'+attr['href']
attr=e[0].getchildren()[0].attrib
attr['src']='/path/'+attr['src']

print(html.tostring(e, pretty_print=True).decode())


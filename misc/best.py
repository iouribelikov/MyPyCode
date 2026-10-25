#!/usr/bin/python3

#print("Content-type: text/html\n\n")


def boiler(extract):

    def inner(files):
        page = """
     <!DOCTYPE html>
     <html lang="en">
     <head>
     <title>Iouri Belikov's best astronomy photos</title>
     
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <meta name="keywords" content="astronomy, galaxy, photography, DSLR">
     <meta name="description" content="Iouri Belikov's best">
     <meta name="author" content="Iouri Belikov">
    
     <link rel="stylesheet" type="text/css" href="../astronomy.css">
     </head>
     
     <body>
     
     <div>
     <h1>My best astronomy photos</h1>
     </div>
     <br>
     """
        page += extract(files)
        page += """
     </body>
     </html>
     """
        return page

    return inner


@boiler
def extract_ids(files):
    element = ''
    for file in files:
        name = file[0] + file[1]
        with open(name) as f:
            for id in file[2]:
                start = False
                for line in f:
                    if 'id=' + id in line:
                        start = True
                    if start and '</div>' in line:
                        start = False
                        element += '</div><hr><br><br>\n\n'
                        break
                    if start:
                        for src in ['src="', 'href="']:
                            if src in line:  #modify the relative path
                                if not 'http' in line:  #do not modify remote paths
                                    index = line.find(src) + len(src)
                                    line = line[:index] + file[0] + line[index:]
                        element += line
    return element


################
if __name__ == '__main__':
    print(
        extract_ids([
            ('../DeepSky/Galaxies/', 'index.html', ['"M101"', '"NGC4565"']),
            ('../DeepSky/Nebulas/', 'index.html', ['"Crab"', '"Horse"'])
        ]))

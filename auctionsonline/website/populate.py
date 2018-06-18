from website.models import *

Product.objects.all().delete()

a = Product()
a.title = "PS4 Pro 1TB"
a.description = "Sony's PS4 Pro 1TB"
a.quantity = 8
a.image.save('console-01.png', File(open('static/images/console-01.png', 'rb')))

a = Product()
a.title = "PS4 Slim 500GB (Gold)"
a.description = "Sony's PS4 Slim Gold Edition with 500GB"
a.quantity = 1
a.image.save('console-02.png', File(open('static/images/console-02.png', 'rb')))

a = Product()
a.title = "PS4 Pro 1TB"
a.description = "Sony's PS4 Pro 1TB"
a.quantity = 8
a.image.save('console-01.png', File(open('static/images/console-01.png', 'rb')))

a = Product()
a.title = "PS4 Pro 1TB"
a.description = "Sony's PS4 Pro 1TB"
a.quantity = 8
a.image.save('console-01.png', File(open('static/images/console-01.png', 'rb')))


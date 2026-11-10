from pathlib import Path
from shutil import copy2
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Preformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report/lab8-canvas-variant5.pdf'
DESKTOP=Path('/Users/maksimginchak/Desktop/Лабораторні/HTML/Лаба 8 Canvas варіант 5.pdf')
pdfmetrics.registerFont(TTFont('ArialUA','/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('ArialUA',normal='ArialUA',bold='ArialBold')
pdfmetrics.registerFont(TTFont('CourierUA','/System/Library/Fonts/Supplemental/Courier New.ttf'))
BLUE=colors.HexColor('#174a7e'); LINE=colors.HexColor('#c9d8e2'); PALE=colors.HexColor('#f2f8fb')
body=ParagraphStyle('body',fontName='ArialUA',fontSize=10.5,leading=16,spaceAfter=8)
heading=ParagraphStyle('heading',fontName='ArialBold',fontSize=13,leading=18,textColor=BLUE,spaceBefore=5,spaceAfter=9)
example=ParagraphStyle('example',parent=heading,fontSize=14,leading=19,spaceAfter=11)
small=ParagraphStyle('small',parent=body,fontSize=10,leading=14)
cell=ParagraphStyle('cell',parent=body,fontSize=9,leading=13,spaceAfter=0)
white=ParagraphStyle('white',parent=cell,fontName='ArialBold',textColor=colors.white)
code=ParagraphStyle('code',fontName='CourierUA',fontSize=8,leading=10)
WIDTH=470.5512
story=[]
def p(s,style=body): return Paragraph(s,style)
def h(s): story.append(p(s,heading))
def paragraph(s,style=body): story.append(p(s,style))
def screenshot(name):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 story.append(Image(str(path),width=WIDTH,height=ht*WIDTH/w))
 story.append(Spacer(1,10))
def source(text):
 block=Preformatted(text.strip(),code)
 t=Table([[block]],colWidths=[WIDTH],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
 story.append(t);story.append(Spacer(1,10))
def page(): story.append(PageBreak())
def example_start(title):
 story.append(p(title,example))
 story.append(p('Сторінка: javascript.html. Скріншот реального сайту у Chrome, ширина вікна 1280 px.',small))


import json
results=json.loads((ROOT/'report/check-results.json').read_text())
def grid(rows,widths):
 t=Table([[p(escape(str(s)),white if i==0 else cell) for s in row] for i,row in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,10))
def image_fit(name,max_height):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 width=min(WIDTH,max_height*w/ht)
 story.append(Image(str(path),width=width,height=ht*width/w,hAlign='LEFT'));story.append(Spacer(1,10))


story.append(Spacer(1,680));page()
h('Завдання та варіант №5')
paragraph('Розробити вебсторінку, на якій геометричні фігури варіанта №5 з лабораторної №6 намальовано на полотні canvas. Запрограмувати подію, за якої вибрані фігури трансформуються та переміщуються.')
h('Побудова малюнка')
paragraph('Відтворено 9 синіх фігур із чорним контуром. Два кола мають радіус 1 і центри (-2; 1), (1; 1). Ромб має вершини (2; -1), (3; 0), (4; -1), (3; -2). Шість прямокутників займають ті самі області, що й у SVG попередньої роботи. Осі X та Y, стрілки, поділки й підписи намальовано командами Canvas.')
source('''const context = canvas.getContext("2d");
context.translate(290, 245);
context.scale(72, -72);''')
paragraph('Початок математичних координат перенесено в точку (290; 245). Одна одиниця дорівнює 72 одиницям полотна. Від’ємний масштаб по Y спрямовує додатну вісь вгору. Текст і осі малюються після відновлення звичайної системи координат.')
h('Основні засоби')
grid([['Засіб','Призначення'],['canvas, getContext("2d")','Полотно та двовимірний контекст малювання.'],['beginPath, arc, rect, lineTo','Новий контур, кола, прямокутники й сторони ромба.'],['fill, stroke, fillStyle, strokeStyle','Синя заливка та чорна обводка.'],['translate, rotate, scale','Переміщення, обертання та зміна розміру.'],['save, restore','Окремі перетворення для кожної фігури.']],[160,WIDTH-160])
h('Файли проєкту')
paragraph('canvas.html містить полотно та форму керування. assets/js/canvas.js зберігає фігури й виконує перемальовування. assets/css/canvas.css задає адаптивний вигляд. На всіх 10 сторінках є пункт Canvas. Детальні пояснення містяться у report/Захист.md і Зміни_порівняно_з_лаб7.md.')
page()
h('Початковий малюнок варіанта №5')
paragraph('Реальний скриншот полотна у Chrome. Фігури побудовано командами Canvas відповідно до координат вихідного SVG.')
image_fit('canvas-static.png',390)
h('Перевірка відповідності')
paragraph(f'Піксельну маску синьої заливки порівняно з SVG шостої роботи. Коефіцієнт перетину до об’єднання масок становить {results["geometryBlueMaskIoU"]:.4f}. Невеликі відмінності припадають на краї контурів і растеризацію. Кількість, положення та колір фігур відповідають варіанту.')
paragraph('Кожна фігура описана даними типу, центра та розмірів. Кола малюються arc із повним кутом 2π, прямокутники - rect, ромб - чотирма відрізками зі замиканням контуру. Перед кожним повторним малюванням фон полотна заповнюється білим.')
page()
h('Подія переміщення та перетворення')
paragraph('Вибрано ромб. Після натискання «Застосувати» задано зсув X = 0.5, Y = 0.5, кут 45° і масштаб 0.75. Центр ромба зміщується з (3; -1) у (3.5; -0.5).')
image_fit('canvas-transformed.png',260)
image_fit('canvas-controls.png',245)
source('''context.save();
context.translate(figure.x + change.dx, figure.y + change.dy);
context.rotate(change.angle * Math.PI / 180);
context.scale(change.scale, change.scale);
// Побудова контуру вибраної фігури.
context.restore();''')
paragraph('Подія submit скасовує перезавантаження форми й оновлює окремий стан фігури. Обертання відбувається навколо її центра. Кнопка відновлення скидає зміни всіх фігур, а resize повторно малює полотно з урахуванням щільності пікселів.',small)
page()
h('Тестові приклади')
grid([['Перевірка','Результат'],['Початковий вигляд','2 кола, 6 прямокутників, ромб. Синя заливка й правильні координати.'],['Переміщення ромба','X = 0.5, Y = 0.5 змінюють центр на (3.5; -0.5).'],['Обертання й масштаб','Кут 45° і масштаб 0.75 змінюють лише вибрану фігуру.'],['Перемикання фігур','Кожна фігура зберігає власні параметри.'],['Масштаб 0','Введення відхиляється стандартною перевіркою форми.'],['Відновлення всіх фігур','Растровий результат точно збігається з початковим.'],['Екран 390 px та Retina','Нова сторінка без горизонтального виходу. Retina має подвоєний розмір буфера.'],['JavaScript вимкнено','Є повідомлення про необхідність сценаріїв, кнопки вимкнено.'],['Навігація',f'{results["htmlPages"]} сторінок і {results["localLinks"]} локальних посилань перевірено. Помилок виконання у Chrome немає.']],[160,WIDTH-160])
h('Що показати під час захисту')
paragraph('Відкрити canvas.html через пункт Canvas. Показати початкові фігури, вибрати ромб і застосувати приклад параметрів. Перемкнутися на коло та показати незалежність станів. Натиснути «Відновити всі фігури». У коді показати canvas, getContext, arc, rect, translate, rotate, scale, save та restore.')
story.append(KeepTogether([p('Висновки',heading),p('Створено Canvas-сторінку з фігурами варіанта №5 та обробкою події перетворення. Реалізовано зсув, поворот, масштабування й повернення до початкового стану. Перевірено відповідність координатам SVG, незалежність фігур та адаптивний вигляд. Основна зміна порівняно з №7 - побудова растрової графіки командами JavaScript.'),p('Репозиторій',heading),p('<link href="https://github.com/MaksHinchak/html-lab-08-variant-5" color="#174a7e">https://github.com/MaksHinchak/html-lab-08-variant-5</link>')]))

def decorate(c,doc):
 c.setFont('ArialUA',9); c.setFillColor(colors.HexColor('#587083'))
 c.drawRightString(538.9134,34,str(doc.page))
 if doc.page==1:
  c.setFillColor(colors.black);c.setFont('ArialUA',12)
  for y,line in [(688.89,'Чернівецький національний університет'),(669.89,'імені Юрія Федьковича'),(650.89,'Навчально-науковий інститут фізико-технічних'),(631.89,'та комп’ютерних наук')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',17)
  for y,line in [(495.89,'ЗВІТ'),(470.89,'про виконання лабораторної роботи №8'),(445.89,'з дисципліни «Веб-програмування»')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',12);c.drawCentredString(A4[0]/2,423.89,'Тема: Растрова графіка Canvas')
  author_lines=[(303.39,'Виконав: студент групи 241-А'),(284.39,'Гінчак Максим Богданович'),(265.39,'Перевірив:'),(246.39,'асистент Нестеренко Володимир Васильович')]
  for y,line in author_lines: c.drawRightString(538.9134,y,line)
  c.drawCentredString(A4[0]/2,48,'Чернівці · 2026')

SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=62.3622,rightMargin=50.3622,topMargin=56,bottomMargin=46,title='Лабораторна робота №8. Растрова графіка Canvas. Варіант 5',author='Гінчак Максим Богданович').build(story,onFirstPage=decorate,onLaterPages=decorate)
r=PdfReader(OUT)
assert len(r.pages)==5,len(r.pages)
assert 'Висновки' in r.pages[-1].extract_text()
assert 'Репозиторій' in r.pages[-1].extract_text()
assert all('Висновки' not in p.extract_text() and 'Репозиторій' not in p.extract_text() for p in r.pages[:-1])
for index,page_obj in enumerate(r.pages):
 assert len(page_obj.extract_text())>50
 assert abs(float(page_obj.mediabox.width)-A4[0])<1
links=[a.get_object().get('/A',{}).get('/URI') for pg in r.pages for a in pg.get('/Annots',[])]
assert 'https://github.com/MaksHinchak/html-lab-08-variant-5' in links
copy2(OUT,DESKTOP)
assert OUT.read_bytes()==DESKTOP.read_bytes()
print(f'Created {len(r.pages)}-page A4 report:',DESKTOP)

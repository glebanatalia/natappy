
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4,landscape

pdfmetrics.registerFont(TTFont('Lato-Lig', 'Lato-Lig.ttf'))
pdfmetrics.registerFont(TTFont('Lato-Reg', 'Lato-Reg.ttf'))
from reportlab.pdfbase.pdfmetrics import stringWidth
   
layouts_positions={'B':{'landscape_positions':[[150,100,521,350]],'portrait_positions':[]},
                   'A':{'landscape_positions':[],'portrait_positions':[[300,50,301,400]]},
                   'BB':{'landscape_positions':[[50,200,350,250],[430,50,350,250]],'portrait_positions':[]},
                   'AA':{'landscape_positions':[],'portrait_positions':[[100,50,301,400],[450,50,301,400]]},                         
                   'AB':{'landscape_positions':[[430,200,350,250]],'portrait_positions':[[100,50,301,400]]}, 
                   'AAA':{'landscape_positions':[],'portrait_positions':[[30,50,251,380],[298,50,251,380],[570,50,251,380]]},  
                   'BBB':{'landscape_positions':[[50,240,350,220],[430,240,350,220],[210,30,350,200]],'portrait_positions':[]}, 
                   'ABB': {'landscape_positions':[[430,260,350,200],[430,50,350,200]],'portrait_positions':[[100,50,300,400]]},     
                   'AAB':{'landscape_positions':[[530,270,290,180]],'portrait_positions':[[30,80,230,370],[280,80,230,370]]}, 
                   'AAAA':{'landscape_positions':[],'portrait_positions':[[30,60,190,330],[230,60,190,330],[430,60,190,330],[630,60,190,330]]}, 
                   'BBBB':{'landscape_positions':[[50,240,350,220],[430,240,350,220],[50,30,350,200],[430,30,350,200]],'portrait_positions':[]},
                   'AABB':{'landscape_positions':[[530,270,290,180],[530,50,290,200]],'portrait_positions':[[30,50,230,400],[280,50,230,400]]},
                   'AAAB':{'landscape_positions':[[475,300,350,200]],'portrait_positions':[[20,40,222,350],[250,40,216,350],[475,40,180,250]]},
                   'ABBB':{'landscape_positions':[[240,250,280,200],[530,250,280,200],[350,50,350,180]],'portrait_positions':[[30,50,200,400]]},
                   'AAAAA':{'landscape_positions':[],'portrait_positions':[[20,225,150,200],[20,20,150,200],[180,50,205,365],[395,50,205,365],[610,50,205,365]]},        
                   'BBBBB':{'landscape_positions':[[20,250,260,200],[290,250,260,200],[50,30,350,200],[420,30,350,200],[560,250,260,200]],'portrait_positions':[]},  
                   'ABBBB':{'landscape_positions':[[20,250,260,200],[290,250,260,200],[20,30,260,200],[290,30,260,200],[560,30,260,420]],'portrait_positions':[[560,30,260,420]]}, 
                   'AAAAB':{'landscape_positions':[[235,260,372,180]],'portrait_positions':[[15,30,210,380],[235,30,180,220],[425,30,180,220],[618,30,207,380]]},
                   'AABBB':{'landscape_positions':[[460,15,320,185],[458,390,320,185],[460,205,320,180]],'portrait_positions':[[20,20,212,370],[240,20,212,370]]},
                   'AAABB':{'landscape_positions':[[100,275,300,185],[410,275,300,185]],'portrait_positions':[[100,20,180,245],[320,20,180,245],[530,20,180,245]]},
                   'AaAaAaAaAa':{'landscape_positions':[],'portrait_positions':[[15,15,170,560],[190,15,165,560],[360,140,151,435],[518,140,151,435],[675,140,148,435]]},
                   'AaAaAaAa':{'landscape_positions':[],'portrait_positions':[[30,120,190,400],[230,120,190,400],[430,120,190,400],[630,120,190,400]]},
                    'AaAaAaAaAaAaAaAa':{'landscape_positions':[],'portrait_positions':[[10,140,100,400],[115,140,100,400],[220,140,100,400],[325,140,100,400],[430,140,100,400],[535,140,100,400],[640,140,100,400],[745,140,100,400]]}}


def stringWidth2(string, font='Lato-Lig', size=24, charspace=0):
    width = stringWidth(string,'Lato-Lig', 24)
    width += (len(string) - 1) * charspace
    return width






def main(rep,blogger,link):
    if link=='':
        rep.setPageSize(landscape(A4))
        rep.rect(0,0,835,500,fill=1)
        rep.setFillGray(0.3) 
        rep.rect(0,0,830,580,stroke=0,fill=1)
        rep.setFillColor('white')
        rep.rect(0,470,450,60,stroke=0,fill=1)
        rep.setFillColor('black')
        rep.setFont("Lato-Lig", 14)
        social_media_position=245-stringWidth2('Social media', font='Lato-Reg', size=16, charspace=0)/2
        rep.drawString(social_media_position,480,'Social media')       
        rep.setFont("Lato-Reg", 16)
        blogger_position=255-stringWidth2(blogger.upper(), font='Lato-Reg', size=16, charspace=0)/2
        rep.drawString(blogger_position,500,blogger.upper())
    else:
        link=link.lstrip('http://www.').rstrip('/')
        rep.setFont("Lato-Lig", 14)
        rep.setPageSize(landscape(A4))
        rep.setFont("Lato-Reg", 16)
        rep.rect(0,0,835,500,fill=1)
        rep.setFillGray(0.3) 
        rep.rect(0,0,830,580,stroke=0,fill=1)
        rep.setFillColor('white')
        rep.rect(360,20,550,90,stroke=0,fill=1)
        rep.setFillColor('black')
        blogger_position=630-stringWidth2(blogger.upper(), font='Lato-Reg', size=16, charspace=0)/2
        rep.drawString(blogger_position,80,blogger.upper())
        rep.setFont("Lato-Lig", 14)
        rep.drawString(570,60,'Blog Post')
        rep.setFont("Lato-Lig", 13)
        social_media_position=650-stringWidth2(link, font='Lato-Lig', size=13, charspace=0)/2
        rep.drawString(social_media_position,40,link)
    rep.setFillColor('white')



def do_a_page(rep,blogger,screens,layout,link='',blogposts=False):
    main(rep,blogger,link)
    print ('layout:', layout)
  #  portrait_positions=layouts_positions[layout]['portrait_positions']
  #  landscape_positions=layouts_positions[layout]['landscape_positions']
  #  counter=0
#    if blogposts:
#        for screen in screens:            
#            try:
#                rep.drawImage(screen,portrait_positions[counter][0],portrait_positions[counter][1],portrait_positions[counter][2],portrait_positions[counter][3])
#            except:
#                rep.setFillGray(0.3)
#                rep.rect(portrait_positions[counter][0],portrait_positions[counter][1],portrait_positions[counter][2],portrait_positions[counter][3],stroke=0,fill=1)               
#            counter+=1
#        
#    else:
#        counter=0   
#        for screen in screens:
#            if screens[screen]['position']=='portrait':
#                try:
#                    rep.drawImage(screen,portrait_positions[counter][0],portrait_positions[counter][1],portrait_positions[counter][2],portrait_positions[counter][3])
#                except:
#                    rep.setFillGray(0.3)
#                    rep.rect(portrait_positions[counter][0],portrait_positions[counter][1],portrait_positions[counter][2],portrait_positions[counter][3],stroke=0,fill=1)               
#                counter+=1
#     
#        counter=0
#        for screen in screens:
#            if screens[screen]['position']=='landscape':
#                try:
#                    rep.drawImage(screen,landscape_positions[counter][0],landscape_positions[counter][1],landscape_positions[counter][2],landscape_positions[counter][3])
#                except:
#                    rep.setFillGray(0.3)
#                    rep.rect(landscape_positions[counter][0],landscape_positions[counter][1],landscape_positions[counter][2],landscape_positions[counter][3],stroke=0,fill=1)                
#                counter+=1
    rep.showPage()
 
    


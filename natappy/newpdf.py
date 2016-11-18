# -*- coding: utf-8 -*-

from os.path import expanduser
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
home = expanduser("~")
import math
from contextlib import suppress
pdfmetrics.registerFont(TTFont('Lato-Lig', 'Lato-Lig.ttf'))
pdfmetrics.registerFont(TTFont('Lato-Reg', 'Lato-Reg.ttf'))
from PIL import Image
from time import gmtime, strftime
import layouts
import pandas


def screenname_to_linkname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b['Blogger'] == blogger][media])[0]


def linkname_to_screenname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b[media] == blogger]['Blogger'])[0]


def blogger_screenshots(dirname, blogger, all_media):
    screenshots_paths = {}
    for media in all_media.keys():
        if screenname_to_linkname(blogger, media) in all_media[media].keys():
            for post in all_media[media][screenname_to_linkname(blogger, media)].keys():
                post_path = '%s/Desktop/%s/%s_screenshots/%s.png' % (home, dirname, media, post)
                with suppress(Exception):
                    img = Image.open(post_path)
                    ratio = img.size[0] / img.size[1]
                    if ratio <= 1:
                        position = 'portrait'
                    if ratio > 1:
                        position = 'landscape'
                    screenshots_paths[post_path] = {'width': img.size[
                        0], 'height': img.size[1], 'position': position}
    return screenshots_paths


def choose_screenshots_layout(screenshots_paths):
    how_many_screens = len(screenshots_paths)
    how_many_pages = math.ceil(how_many_screens / 5)
    counter = 0
    layout = {}
    counter = 0
    for el in screenshots_paths.keys():
        layout[el] = {'counter': counter, 'width': screenshots_paths[
            el]['width'], 'position': screenshots_paths[el]['position']}
        counter += 1
    final_layout = {}
    for i in range(how_many_pages):
        final_layout[i] = {}
    for el in layout:
        final_layout[math.floor(layout[el]['counter'] / 5)][el] = layout[el]
    return final_layout


def page_layout(final_layout_line):
    pagetype = ''
    if type(final_layout_line) is not int:
        for el in final_layout_line:
            if final_layout_line[el]['position'] == 'portrait':
                pagetype += 'A'
            if final_layout_line[el]['position'] == 'landscape':
                pagetype += 'B'
    new_pagetype = ''.join(sorted([letter for letter in pagetype]))
    return new_pagetype, final_layout_line


def blogger_likes_count(media, blogger, all_media):
    return sum(all_media[media][screenname_to_linkname(blogger, media)][post]['likes'] for post in all_media[media][screenname_to_linkname(blogger, media)].keys())


def blogger_comments_count(media, blogger, all_media):
    return sum(all_media[media][screenname_to_linkname(blogger, media)][post]['comments'] for post in all_media[media][screenname_to_linkname(blogger, media)].keys())


def blogger_shares_count(media, blogger, all_media):
    return sum(all_media[media][screenname_to_linkname(blogger, media)][post]['shares'] for post in all_media[media][screenname_to_linkname(blogger, media)].keys())


def blogger_interactions_count(media, blogger, all_media):
    return blogger_likes_count(media, blogger, all_media) + blogger_comments_count(media, blogger, all_media) + blogger_shares_count(media, blogger, all_media)


def blogger_rates_count(media, reachtype, blogger, all_media):
    toreturn = 0.00
    if reachtype == 'Applause Rate':
        with suppress(Exception):
            rate = blogger_likes_count(media, blogger, all_media) / \
                len(all_media[media][screenname_to_linkname(blogger, media)])
            return str(("%.2f" % rate))
    if reachtype == 'Conversation Rate':
        with suppress(Exception):
            rate = blogger_comments_count(media, blogger, all_media) / \
                len(all_media[media][screenname_to_linkname(blogger, media)])
            return str(("%.2f" % rate))
    if reachtype == 'Amplification Rate':
        with suppress(Exception):
            rate = blogger_shares_count(media, blogger, all_media) / \
                len(all_media[media][screenname_to_linkname(blogger, media)])
            return str(("%.2f" % rate))
    if reachtype == 'Interaction Rate':
        with suppress(Exception):
            rate = blogger_interactions_count(
                media, blogger, all_media) / len(all_media[media][screenname_to_linkname(blogger, media)])
            return str(("%.2f" % rate))
    return toreturn


def blogger_reach_count(media, reachtype, blogger, all_media, followers_data):
    if reachtype == 'Direct':
        return followers_data[blogger][media]
    if reachtype == 'Indirect':
        return 0
    if reachtype == 'Impressions':
        return followers_data[blogger][media] * len(all_media[media][screenname_to_linkname(blogger, media)])


def blogger_social_media_page(rep, dirname, blogger, all_media):
    screens = blogger_screenshots(dirname, blogger, all_media)
    pages = choose_screenshots_layout(screens)
    for page in pages.keys():
        layout = page_layout(pages[page])[0]
        screens = page_layout(pages[page])[1]
        try:
            layouts.do_a_page(rep, blogger, screens, layout)
        except:
            pass


def Facebook_results_page(rep, bloggers, all_media, followers_data):
    if all_media['Facebook']:
        rep.setFont("Lato-Lig", 24)
        rep.drawString(90, 543, 'FACEBOOK RESULTS')
        rep.line(80, 530, 80, 570)
        rep.rect(20, 470, 805, 40, fill=1)
        rep.setFillColor('white')
        rep.setFont("Lato-Reg", 12)
        rep.drawString(30, 485, 'Influencer')
        rep.drawString(125, 485, 'Posts')
        rep.drawString(165, 485, 'Interactions')
        rep.drawString(245, 485, 'Likes')
        rep.drawString(282, 485, 'Comments')
        rep.drawString(355, 485, 'Shares')
        rep.drawString(400, 490, 'Interaction')
        rep.drawString(415, 478, 'Rate')
        rep.drawString(480, 490, 'Applause')
        rep.drawString(494, 478, 'Rate')
        rep.drawString(545, 490, 'Conversation')
        rep.drawString(565, 478, 'Rate')
        rep.drawString(630, 490, 'Amplification')
        rep.drawString(655, 478, 'Rate')
        rep.drawString(710, 486, 'Reach')
        rep.drawString(753, 486, 'Impressions')
        rep.setFillColor('black')
        counter = 0
        rep.setFont("Lato-Lig", 10)
        rows = len(bloggers)
        for blogger in bloggers:
            try:
                a = len(all_media['Facebook'][screenname_to_linkname(blogger, 'Facebook')])
                if len(all_media['Facebook'][screenname_to_linkname(blogger, 'Facebook')]) != 0:
                    position = 450 - counter
                    rep.drawString(25, position, blogger)
                # try:
                    rep.drawString(135, position, str("{:,}".format(
                        len(all_media['Facebook'][screenname_to_linkname(blogger, 'Facebook')]))))
                    rep.drawString(245, position, str("{:,}".format(
                        blogger_likes_count('Facebook', blogger, all_media))))
                    rep.drawString(300, position, str("{:,}".format(
                        blogger_comments_count('Facebook', blogger, all_media))))
                    rep.drawString(365, position, str("{:,}".format(
                        blogger_shares_count('Facebook', blogger, all_media))))
                    rep.drawString(185, position, str("{:,}".format(
                        blogger_interactions_count('Facebook', blogger, all_media))))
                    rep.drawString(415, position, str(blogger_rates_count(
                        'Facebook', 'Interaction Rate', blogger, all_media)))
                    rep.drawString(490, position, str(blogger_rates_count(
                        'Facebook', 'Applause Rate', blogger, all_media)))
                    rep.drawString(565, position, str(blogger_rates_count(
                        'Facebook', 'Conversation Rate', blogger, all_media)))
                    rep.drawString(650, position, str(blogger_rates_count(
                        'Facebook', 'Amplification Rate', blogger, all_media)))
                    rep.drawString(715, position, str("{:,}".format(blogger_reach_count(
                        'Facebook', 'Direct', blogger, all_media, followers_data))))
                    rep.drawString(763, position, str("{:,}".format(blogger_reach_count(
                        'Facebook', 'Impressions', blogger, all_media, followers_data))))
                    counter += 30
                else:
                    rows -= 1
            except:
                rows -= 1
        table_height = 0
        for i in range(rows + 1):
            rep.line(20, 470 - 30 * i, 825, 470 - 30 * i)
            table_height = 470 - 30 * i
        rep.line(20, 470, 20, table_height)
        rep.line(825, 470, 825, table_height)
        rep.setFillColor('black')
        rep.showPage()
    else:
        pass


def Instagram_results_page(rep, bloggers, all_media, followers_data):
    if all_media['Instagram']:
        rep.setFont("Lato-Lig", 24)
        rep.drawString(90, 543, 'INSTAGRAM RESULTS')
        rep.line(80, 530, 80, 570)

        rep.rect(20, 470, 805, 40, fill=1)
        rep.setFillColor('white')
        rep.setFont("Lato-Reg", 12)

        rep.drawString(25, 485, 'Influencer')
        rep.drawString(140, 485, 'Posts')
        rep.drawString(185, 485, 'Interactions')  # 320
        rep.drawString(270, 485, 'Likes')
        rep.drawString(320, 485, 'Comments')

        rep.drawString(395, 490, 'Interaction')  # 580
        rep.drawString(412, 476, 'Rate')
        rep.drawString(485, 490, 'Applause')  # 395
        rep.drawString(495, 476, 'Rate')
        rep.drawString(570, 490, 'Conversation')
        rep.drawString(590, 476, 'Rate')

        rep.drawString(670, 486, 'Reach')
        rep.drawString(730, 486, 'Impressions')

        rep.setFillColor('black')
        counter = 0
        rep.setFont("Lato-Lig", 10)
        rows = len(bloggers)
        for blogger in bloggers:
            try:
                a = len(all_media['Instagram'][screenname_to_linkname(blogger, 'Instagram')])
                if len(all_media['Instagram'][screenname_to_linkname(blogger, 'Instagram')]) != 0:
                    position = 450 - counter
                    rep.drawString(25, position, blogger)
                    rep.drawString(150, position, str("{:,}".format(
                        len(all_media['Instagram'][screenname_to_linkname(blogger, 'Instagram')]))))
                    rep.drawString(270, position, str("{:,}".format(
                        blogger_likes_count('Instagram', blogger, all_media))))
                    rep.drawString(335, position, str("{:,}".format(
                        blogger_comments_count('Instagram', blogger, all_media))))
                    rep.drawString(190, position, str("{:,}".format(
                        blogger_interactions_count('Instagram', blogger, all_media))))
                    rep.drawString(490, position, str(blogger_rates_count(
                        'Instagram', 'Applause Rate', blogger, all_media)))
                    rep.drawString(590, position, str(blogger_rates_count(
                        'Instagram', 'Conversation Rate', blogger, all_media)))
                    rep.drawString(410, position, str(blogger_rates_count(
                        'Instagram', 'Interaction Rate', blogger, all_media)))
                    rep.drawString(670, position, str("{:,}".format(blogger_reach_count(
                        'Instagram', 'Direct', blogger, all_media, followers_data))))
                    rep.drawString(736, position, str("{:,}".format(blogger_reach_count(
                        'Instagram', 'Impressions', blogger, all_media, followers_data))))
                    counter += 30
                else:
                    rows -= 1
            except:
                rows -= 1
        table_height = 0
        for i in range(rows + 1):
            rep.line(20, 470 - 30 * i, 825, 470 - 30 * i)
            table_height = 470 - 30 * i
        rep.line(20, 470, 20, table_height)
        rep.line(825, 470, 825, table_height)
        rep.showPage()
    else:
        pass


def Twitter_results_page(rep, bloggers, all_media, followers_data):
    if all_media['Twitter']:
        rep.setFont("Lato-Lig", 24)
        rep.drawString(90, 543, 'TWITTER RESULTS')
        rep.line(80, 530, 80, 570)
        rep.rect(20, 470, 805, 40, fill=1)
        rep.setFillColor('white')
        rep.setFont("Lato-Reg", 12)
        rep.drawString(30, 485, 'Influencer')
        rep.drawString(140, 485, 'Posts')
        rep.drawString(190, 485, 'Interactions')  # 320
        rep.drawString(273, 485, 'Likes')
        rep.drawString(320, 485, 'Retweets')  # 240

        rep.drawString(395, 490, 'Interaction')  # 585
        rep.drawString(407, 476, 'Rate')

        rep.drawString(490, 490, 'Applause')  # 395
        rep.drawString(500, 476, 'Rate')
        rep.drawString(570, 490, 'Amplification')
        rep.drawString(591, 476, 'Rate')

        rep.drawString(670, 486, 'Reach')
        rep.drawString(730, 486, 'Impressions')
        rep.setFillColor('black')
        counter = 0
        rep.setFont("Lato-Lig", 10)
        rows = len(bloggers)
        for blogger in bloggers:
            try:
                a = len(all_media['Twitter'][screenname_to_linkname(blogger, 'Twitter')])
                if len(all_media['Twitter'][screenname_to_linkname(blogger, 'Twitter')]) != 0:
                    position = 450 - counter
                    rep.drawString(25, position, blogger)
                    rep.drawString(150, position, str("{:,}".format(
                        len(all_media['Twitter'][screenname_to_linkname(blogger, 'Twitter')]))))
                    rep.drawString(278, position, str("{:,}".format(
                        blogger_likes_count('Twitter', blogger, all_media))))
                    rep.drawString(332, position, str("{:,}".format(
                        blogger_shares_count('Twitter', blogger, all_media))))
                    rep.drawString(203, position, str("{:,}".format(
                        blogger_interactions_count('Twitter', blogger, all_media))))
                    rep.drawString(502, position, str(blogger_rates_count(
                        'Twitter', 'Applause Rate', blogger, all_media)))
                    rep.drawString(590, position, str(blogger_rates_count(
                        'Twitter', 'Amplification Rate', blogger, all_media)))
                    rep.drawString(410, position, str(blogger_rates_count(
                        'Twitter', 'Interaction Rate', blogger, all_media)))
                    rep.drawString(675, position, str("{:,}".format(blogger_reach_count(
                        'Twitter', 'Direct', blogger, all_media, followers_data))))
                    rep.drawString(740, position, str("{:,}".format(blogger_reach_count(
                        'Twitter', 'Impressions', blogger, all_media, followers_data))))
                    counter += 30
                else:
                    rows -= 1
            except:
                rows -= 1
        table_height = 0
        for i in range(rows + 1):
            rep.line(20, 470 - 30 * i, 825, 470 - 30 * i)
            table_height = 470 - 30 * i
        rep.line(20, 470, 20, table_height)
        rep.line(825, 470, 825, table_height)
        rep.setFillColor('black')
        rep.showPage()
    else:
        pass


def stringWidth2(string, font='Lato-Lig', size=24, charspace=0):
    width = stringWidth(string, 'Lato-Lig', 24)
    width += (len(string) - 1) * charspace
    return width


def welcome_pages(rep, brand, campaign):
    rep.drawImage('%s/Desktop/natappy/images/first.png' %
                  home, 200, 280, 470, 213)  # 260,320,300,100
    rep.setFont('Lato-Lig', 24)
    brand = ' '.join([letter.upper() for letter in brand])
    brand_position = 421 - stringWidth2(brand, font='Lato-Lig', size=24, charspace=0) / 2
    campaign = ' '.join([letter.upper() for letter in campaign])
    campaign_position = 421 - stringWidth2(campaign, font='Lato-Lig', size=24, charspace=0) / 2
    rep.drawString(brand_position, 200, brand)
    rep.drawString(campaign_position, 140, campaign)
    rep.drawString(240, 80, "P O S T  C A M P A I G N  R E P O R T")
    rep.showPage()
    rep.drawImage('%s/Desktop/natappy/images/WIW.png' % home, 320, 380, 200, 130)
    rep.setFont('Lato-Lig', 12)
    rep.drawString(
        160, 300, 'WaR is a diverse digital network consisting of bespoke bloggers and online magazines. WaR presents a')
    rep.drawString(
        167, 270, 'unique and engaging fashion environment speaking to an opinion forming audience of trend-setters.')
    rep.drawString(
        160, 240, 'WaR aligns brands with influential fashion writers and internationally recognised publishers elevating')
    rep.drawString(240, 210, 'brand profiles through on brand advertising and content campaigns.')
    rep.setFont('Lato-Reg', 14)
    rep.drawString(360, 150, 'www.war-network.com')
    rep.line(160, 100, 700, 100)
    rep.showPage()


def screenname_to_website(blogger):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b['Blogger'] == blogger]['URL'])[0]


def screenname_to_visits(blogger):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return int(list(b[b['Blogger'] == blogger]['Uniques'])[0])


def three_site_statistic_page(rep, all_media, followers_data, bloggers):
    rep.setPageSize((842, 650))
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 600, 'SITE STATISTIC')
    rep.line(80, 590, 80, 620)
    rep.rect(20, 500, 805, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(40, 515, "Site")
    if 'Instagram' in all_media:
        rep.drawString(420, 515, 'Instagram')
    if 'Twitter' in all_media:
        rep.drawString(530, 515, 'Twitter')
    if 'Facebook' in all_media:
        rep.drawString(640, 515, 'Facebook')
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(20, 470 - 30 * i, 825, 470 - 30 * i)
        table_height = 470 - 30 * i
    rep.line(20, 500, 20, table_height)
    rep.line(825, 500, 825, table_height)
    rep.setFillColor('black')
    rep.setFont('Lato-Lig', 12)
    counter = 0
    for blogger in bloggers:
        position = 480 - counter
        rep.drawString(30, position, blogger)
        with suppress(Exception):
            rep.drawString(660, position, str("{:,}".format(followers_data[blogger]['Facebook'])))
        with suppress(Exception):
            rep.drawString(420, position, str("{:,}".format(followers_data[blogger]['Instagram'])))
        with suppress(Exception):
            rep.drawString(530, position, str("{:,}".format(followers_data[blogger]['Twitter'])))
        counter += 30
    rep.showPage()
    rep.setPageSize(landscape(A4))


def two_site_statistic_page(rep, all_media, followers_data, bloggers):
    media1 = 'Instagram' if 'Instagram' in all_media.keys() else 'Twitter'
    media2 = [media for media in list(all_media.keys()) if media != media1][0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 400, 805, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(60, 415, "Site")
    rep.drawString(420, 415, media1)
    rep.drawString(630, 415, media2)
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(20, 370 - 30 * i, 825, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(20, 400, 20, table_height)
    rep.line(825, 400, 825, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 14)
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(30, position, blogger)
        with suppress(Exception):
            rep.drawString(420, position, str("{:,}".format(followers_data[blogger][media1])))
        with suppress(Exception):
            rep.drawString(630, position, str("{:,}".format(followers_data[blogger][media2])))
        counter += 30
    rep.showPage()


def one_site_statistic_page(rep, all_media, followers_data, bloggers):
    media1 = list(all_media.keys())[0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(230, 400, 400, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(240, 415, "Site")
    rep.drawString(550, 415, media1)
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(230, 370 - 30 * i, 630, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(230, 400, 230, table_height)
    rep.line(630, 400, 630, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 14)
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(240, position, blogger)
        with suppress(Exception):
            rep.drawString(550, position, str("{:,}".format(followers_data[blogger][media1])))
        counter += 30
    rep.showPage()


def one_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers):
    media1 = list(all_media.keys())[0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 400, 805, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(40, 415, "Site")
    rep.drawString(200, 415, 'URL')
    rep.drawString(480, 415, 'Unique Viewers p/m')
    rep.drawString(710, 415, media1)
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(20, 370 - 30 * i, 825, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(20, 400, 20, table_height)
    rep.line(825, 400, 825, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 14)
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(30, position, blogger)
        with suppress(Exception):
            rep.drawString(715, position, str("{:,}".format(followers_data[blogger][media1])))
        with suppress(Exception):
            rep.drawString(510, position, str("{:,}".format(screenname_to_visits(blogger))))
      #  with suppress(Exception):
        rep.drawString(200, position, screenname_to_website(blogger))
        counter += 30
    rep.showPage()


def three_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers):
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 400, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(40, 415, "Site")
    rep.drawString(200, 415, 'URL')
    rep.drawString(380, 415, 'Unique Viewers p/m')
    if 'Instagram' in all_media:
        rep.drawString(520, 415, 'Instagram')
    if 'Twitter' in all_media:
        rep.drawString(630, 415, 'Twitter')
    if 'Facebook' in all_media:
        rep.drawString(740, 415, 'Facebook')
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(20, 370 - 30 * i, 825, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(20, 400, 20, table_height)
    rep.line(825, 400, 825, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 12)
    for blogger in bloggers:
        position = 380 - counter
     #   with suppress(Exception):
        rep.drawString(200, position, str(screenname_to_website(blogger)))
      #  with suppress(Exception):
        rep.drawString(420, position, str("{:,}".format(screenname_to_visits(blogger))))
        counter += 30
    counter = 0
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(30, position, blogger)
        with suppress(Exception):
            rep.drawString(750, position, str("{:,}".format(followers_data[blogger]['Facebook'])))
        with suppress(Exception):
            rep.drawString(530, position, str("{:,}".format(followers_data[blogger]['Instagram'])))
        with suppress(Exception):
            rep.drawString(640, position, str("{:,}".format(followers_data[blogger]['Twitter'])))

        counter += 30
    rep.showPage()


def two_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers):
    media1 = 'Instagram' if 'Instagram' in all_media.keys() else 'Twitter'
    media2 = [media for media in list(all_media.keys()) if media != media1][0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 400, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(40, 415, "Site")
    rep.drawString(200, 415, 'URL')
    rep.drawString(400, 415, 'Unique Viewers p/m')
    rep.drawString(570, 415, media1)
    rep.drawString(700, 415, media2)

    table_height = 0
    for i in range(len(bloggers)):
        rep.line(20, 370 - 30 * i, 825, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(20, 400, 20, table_height)
    rep.line(825, 400, 825, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 12)
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(200, position, str(screenname_to_website(blogger)))
        rep.drawString(440, position, str("{:,}".format(screenname_to_visits(blogger))))
        counter += 30
    counter = 0
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(30, position, blogger)
        with suppress(Exception):
            rep.drawString(715, position, str("{:,}".format(followers_data[blogger][media2])))
        with suppress(Exception):
            rep.drawString(580, position, str("{:,}".format(followers_data[blogger][media1])))
        counter += 30
    rep.showPage()


def blogs_only_statistic_page(rep, all_media, followers_data, bloggers):
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SITE STATISTIC')
    rep.line(80, 530, 80, 570)
    rep.rect(70, 400, 705, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(120, 415, "Site")
    rep.drawString(350, 415, 'URL')
    rep.drawString(600, 415, 'Unique Viewers p/m')
    table_height = 0
    for i in range(len(bloggers)):
        rep.line(70, 370 - 30 * i, 775, 370 - 30 * i)
        table_height = 370 - 30 * i
    rep.line(70, 400, 70, table_height)
    rep.line(775, 400, 775, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont('Lato-Lig', 12)
    for blogger in bloggers:
        position = 380 - counter
        rep.drawString(120, position, blogger)
        rep.drawString(350, position, str(screenname_to_website(blogger)))
        rep.drawString(630, position, str("{:,}".format(screenname_to_visits(blogger))))
        counter += 30
    counter = 0
    rep.showPage()


def site_statistic_page(rep, all_media, followers_data, bloggers, platforms):
    if len(all_media.keys()) == 3 and not 'Blogs' in platforms:
        three_site_statistic_page(rep, all_media, followers_data, bloggers)
    if len(all_media.keys()) == 3 and 'Blogs' in platforms:
        three_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers)
    if len(all_media.keys()) == 2 and not 'Blogs' in platforms:
        two_site_statistic_page(rep, all_media, followers_data, bloggers)
    if len(all_media.keys()) == 2 and 'Blogs' in platforms:
        two_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers)
    if len(all_media.keys()) == 1 and not 'Blogs' in platforms:
        one_site_statistic_page(rep, all_media, followers_data, bloggers)
    if len(all_media.keys()) == 1 and 'Blogs' in platforms:
        one_site_plus_blog_statistic_page(rep, all_media, followers_data, bloggers)
    if platforms == ['Blogs']:
        blogs_only_statistic_page(rep, all_media, followers_data, bloggers)


def media_posts_count(media, all_media):
    return sum(int(len(all_media[media][blogger].keys())) for blogger in all_media[media].keys())


def media_likes_count(media, all_media):
    return sum(data['likes'] for blogger in all_media[media] for media_key, data in all_media[media][blogger].items())


def media_comments_count(media, all_media):
    return sum(data['comments'] for blogger in all_media[media] for media_key, data in all_media[media][blogger].items())


def media_shares_count(media, all_media):
    return sum(data['shares'] for blogger in all_media[media] for media_key, data in all_media[media][blogger].items())


def media_interactions_count(media, all_media):
    return media_shares_count(media, all_media) + media_comments_count(media, all_media) + media_likes_count(media, all_media)


def count_media_results(media, metric, all_media):
    if metric == 'Posts':
        return media_posts_count(media, all_media)
    if metric == 'Likes':
        return media_likes_count(media, all_media)
    if metric == 'Comments':
        return media_comments_count(media, all_media)
    if metric == 'Shares':
        return media_shares_count(media, all_media)
    if metric == 'Interactions':
        return media_interactions_count(media, all_media)


def count_media_rates(media, metric, all_media):
    if '.' in metric:
        metric = metric.split('.')[0]
    toreturn = 0.00
    if metric == 'Applause Rate':
        with suppress(Exception):
            rate = media_likes_count(media, all_media) / media_posts_count(media, all_media)
            return str(("%.2f" % rate))
    if metric == 'Conversation Rate':
        with suppress(Exception):
            rate = media_comments_count(media, all_media) / media_posts_count(media, all_media)
            return str(("%.2f" % rate))
    if metric == 'Amplification Rate':
        with suppress(Exception):
            rate = media_shares_count(media, all_media) / media_posts_count(media, all_media)
            return str(("%.2f" % rate))
    if metric == 'Interaction Rate':
        with suppress(Exception):
            rate = media_interactions_count(media, all_media) / media_posts_count(media, all_media)
            return str(("%.2f" % rate))
    return toreturn


def count_total_rates(metric, all_media):
    toreturn = 0.00
    if metric == 'Applause Rate':
        with suppress(Exception):
            rate = sum([media_likes_count(media, all_media) for media in all_media.keys()]) / \
                sum([media_posts_count(media, all_media) for media in all_media.keys()])
            return str(("%.2f" % rate))
    if metric == 'Conversation Rate':
        with suppress(Exception):
            rate = sum([media_comments_count(media, all_media) for media in all_media.keys()]) / \
                sum([media_posts_count(media, all_media) for media in all_media.keys()])
            return str(("%.2f" % rate))
    if metric == 'Amplification Rate':
        with suppress(Exception):
            rate = sum([media_shares_count(media, all_media) for media in all_media.keys()]) / \
                sum([media_posts_count(media, all_media) for media in all_media.keys()])
            return str(("%.2f" % rate))
    if metric == 'Interaction Rate':
        with suppress(Exception):
            rate = sum([media_interactions_count(media, all_media) for media in all_media.keys()]
                       ) / sum([media_posts_count(media, all_media) for media in all_media.keys()])
            return str(("%.2f" % rate))
    return toreturn


def count_media_impression(all_media, media, followers_data, reshares):
    media_impression = 0
    for blogger in all_media[media]:
        try:
            media_impression += followers_data[linkname_to_screenname(
                blogger, media)][media] * len(all_media[media][blogger])
        except:
            pass
    return media_impression + count_reach_from_reposts(reshares, media)


def count_reach_from_reposts(reshares, media):
    if media == 'Instagram':
        return 0
    if not reshares[media]:
        return 0
    else:
        impression = 0
        for blogger in reshares[media].keys():
            for post in reshares[media][blogger].keys():
                for repost in reshares[media][blogger][post].keys():
                    # TODO is it correct
                    impression += reshares[media][blogger][post][repost]['impression']
    return impression


def media_reach(media, metric, followers_data, all_media, reshares):
    if '.' in metric:
        metric = metric.split('.')[0]
    if metric == 'Direct Reach':
        return sum([followers_data[blogger][media] for blogger in followers_data.keys() if followers_data[blogger][media]])
    if metric == 'Indirect Reach':
        return count_reach_from_reposts(reshares, media)
    if metric == 'Impressions':
        return count_media_impression(all_media, media, followers_data, reshares)


def total_reach(metric, followers_data, all_media, reshares):
    if '.' in metric:
        metric = metric.split('.')[0]
    if metric == 'Direct Reach':
        reach = 0
        for blogger in followers_data.keys():
            for media in followers_data[blogger].keys():
                reach += followers_data[blogger][media]
        return reach
    if metric == 'Indirect Reach':
        return sum([count_reach_from_reposts(reshares, media) for media in reshares.keys()])
    if metric == 'Impressions':
        return sum([count_media_impression(all_media, media, followers_data, reshares) for media in all_media])


def one_social_media_reach_page(rep, all_media, followers_data, reshares):
    media1 = list(all_media.keys())[0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SOCIAL MEDIA RESULTS')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 460, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(455, 475, media1)
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 475, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 430 - 30 * i, 825, 430 - 30 * i)
        table_height = 430 - 30 * i
    rep.line(20, 460, 20, table_height)
    rep.line(825, 460, 825, table_height)
    rep.line(650, 460, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interactions', 'Likes/Favourites', 'Comments', 'Shares/Retweets']:
        position = 440 - counter
        if metric in ['Likes/Favourites', 'Comments', 'Shares/Retweets']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Comments':
            if media1 == 'Twitter':
                rep.drawString(465, position, '---')
                rep.drawString(700, position, '---')
            else:
                rep.drawString(465, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
                rep.drawString(700, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
        if metric == 'Shares/Retweets':
            if media1 == 'Instagram':
                rep.drawString(465, position, '---')
                rep.drawString(700, position, '---')
            else:
                rep.drawString(465, position, str("{:,}".format(
                    count_media_results(media1, 'Shares', all_media))))
                rep.drawString(700, position, str("{:,}".format(
                    count_media_results(media1, 'Shares', all_media))))
        if metric in ['Posts', 'Interactions', 'Likes/Favourites']:
            metric = metric.split('/')[0]
            rep.drawString(465, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
            rep.drawString(700, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
        counter += 30
    table_height = 0
    rep.rect(650, 280, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(685, 290, 'Average per post')
    rep.setFillColor('black')
    for i in range(5):
        rep.line(20, 280 - 30 * i, 825, 280 - 30 * i)
        table_height = 280 - 30 * i
    rep.line(20, 280, 20, table_height)
    rep.line(825, 280, 825, table_height)
    rep.line(650, 280, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Interaction Rate.Interaction per post', 'Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
        position = 260 - counter
        if metric in ['Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(55, position - 4, explain)
            rep.setFont("Lato-Reg", 13)
        else:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.drawString(30, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(30, position - 4, explain)
        rep.setFont("Lato-Lig", 13)
        metric = metric.split('.')[0]
        if metric == 'Conversation Rate':
            if media1 == 'Twitter':
                rep.drawString(465, position, '---')
                rep.drawString(700, position, '---')
            else:
                rep.drawString(465, position, str(count_media_rates(media1, metric, all_media)))
                rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        if metric == 'Amplification Rate':
            if media1 == 'Instagram':
                rep.drawString(465, position, '---')
                rep.drawString(700, position, '---')
            else:
                rep.drawString(465, position, str(count_media_rates(media1, metric, all_media)))
                rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        if metric in ['Interaction Rate', 'Applause Rate']:
            rep.drawString(465, position, str(count_media_rates(media1, metric, all_media)))
            rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        counter += 30
    rep.setFillColor('black')
    rep.rect(650, 130, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(700, 140, 'TOTALS')
    rep.setFillColor('black')
    table_height = 0

    table_height = 0
    for i in range(4):
        rep.line(20, 130 - 30 * i, 825, 130 - 30 * i)
        table_height = 130 - 30 * i
    rep.line(20, 130, 20, table_height)
    rep.line(825, 130, 825, table_height)
    rep.line(650, 130, 650, table_height)
    counter = 0
    for metric in ['Direct Reach/Uniques', 'Indirect Reach', 'Impressions']:
        rep.setFont("Lato-Reg", 13)
        position = 110 - counter
        rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        metric = metric.split('/')[0]
        if metric == 'Indirect Reach':
            if media1 == 'Instagram':
                rep.drawString(465, position, '---')
                rep.drawString(700, position, '---')
            else:
                rep.drawString(465, position, str("{:,}".format(media_reach(
                    media1, metric, followers_data, all_media, reshares))))
                rep.drawString(700, position, str("{:,}".format(
                    total_reach(metric, followers_data, all_media, reshares))))
        if metric in ['Direct Reach', 'Impressions']:
            rep.drawString(465, position, str("{:,}".format(media_reach(
                media1, metric, followers_data, all_media, reshares))))
            rep.drawString(700, position, str("{:,}".format(
                total_reach(metric, followers_data, all_media, reshares))))
        counter += 30
    rep.showPage()


def two_social_media_reach_page(rep, all_media, followers_data, reshares):
    media1 = 'Instagram' if 'Instagram' in all_media.keys() else 'Twitter'
    media2 = [media for media in list(all_media.keys()) if media != media1][0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SOCIAL MEDIA RESULTS')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 460, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(310, 475, media1)
    rep.drawString(495, 475, media2)
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 475, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 430 - 30 * i, 825, 430 - 30 * i)
        table_height = 430 - 30 * i
    rep.line(20, 460, 20, table_height)
    rep.line(825, 460, 825, table_height)
    rep.line(650, 460, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interactions', 'Likes/Favourites', 'Comments', 'Shares/Retweets']:
        position = 440 - counter
        if metric in ['Likes/Favourites', 'Comments', 'Shares/Retweets']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Comments':
            if media1 == 'Twitter':
                rep.drawString(330, position, '---')
                rep.drawString(515, position, str("{:,}".format(
                    count_media_results(media2, 'Comments', all_media))))
            if media2 == 'Twitter':
                rep.drawString(515, position, '---')
                rep.drawString(330, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
            if media1 != 'Twitter' and media2 != 'Twitter':
                rep.drawString(330, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
                rep.drawString(515, position, str("{:,}".format(
                    count_media_results(media2, 'Comments', all_media))))

        if metric == 'Shares/Retweets':
            if media1 == 'Instagram':
                rep.drawString(330, position, '---')
                rep.drawString(515, position, str("{:,}".format(
                    count_media_results(media2, 'Shares', all_media))))
            else:
                rep.drawString(330, position, str("{:,}".format(
                    count_media_results(media1, 'Shares', all_media))))
                rep.drawString(515, position, str("{:,}".format(
                    count_media_results(media2, 'Shares', all_media))))

        if metric in ['Interactions', 'Likes/Favourites', 'Posts']:
            metric = metric.split('/')[0]
            rep.drawString(330, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
            rep.drawString(515, position, str("{:,}".format(
                count_media_results(media2, metric, all_media))))
        metric = metric.split('/')[0]
        rep.drawString(700, position, str("{:,}".format(count_media_results(
            media2, metric, all_media) + count_media_results(media1, metric, all_media))))
        counter += 30
    table_height = 0
    rep.rect(650, 280, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(685, 290, 'Average per post')
    rep.setFillColor('black')
    for i in range(5):
        rep.line(20, 280 - 30 * i, 825, 280 - 30 * i)
        table_height = 280 - 30 * i
    rep.line(20, 280, 20, table_height)
    rep.line(825, 280, 825, table_height)
    rep.line(650, 280, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Interaction Rate.Interaction per post', 'Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate. Shares per post']:
        position = 260 - counter
        if metric in ['Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate. Shares per post']:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(55, position - 4, explain)
            rep.setFont("Lato-Reg", 13)
        else:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.drawString(30, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(30, position - 4, explain)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Conversation Rate':
            if media1 == 'Twitter':
                rep.drawString(330, position, '---')
                rep.drawString(515, position, str(count_media_rates(
                    media2, 'Conversation Rate', all_media)))
            if media2 == 'Twitter':
                rep.drawString(515, position, '---')
                rep.drawString(330, position, str(count_media_rates(
                    media1, 'Conversation Rate', all_media)))
            if media1 != 'Twitter' and media2 != 'Twitter':
                rep.drawString(330, position, str(count_media_rates(media1, metric, all_media)))
                rep.drawString(515, position, str(count_media_rates(media2, metric, all_media)))
        if metric == 'Amplification Rate':
            if media1 == 'Instagram':
                rep.drawString(330, position, '---')
                rep.drawString(515, position, str(count_media_rates(
                    media2, 'Amplification Rate', all_media)))
            else:
                rep.drawString(330, position, str(count_media_rates(media1, metric, all_media)))
                rep.drawString(515, position, str(count_media_rates(media2, metric, all_media)))
        if metric in ['Applause Rate', 'Interaction Rate']:
            rep.drawString(330, position, str(count_media_rates(media1, metric, all_media)))
            rep.drawString(515, position, str(count_media_rates(media2, metric, all_media)))
        rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        counter += 30

    rep.setFillColor('black')
    rep.rect(650, 130, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(700, 140, 'TOTALS')
    rep.setFillColor('black')
    table_height = 0
    for i in range(4):
        rep.line(20, 130 - 30 * i, 825, 130 - 30 * i)
        table_height = 130 - 30 * i
    rep.line(20, 130, 20, table_height)
    rep.line(825, 130, 825, table_height)
    rep.line(650, 130, 650, table_height)
    counter = 0
    for metric in ['Direct Reach', 'Indirect Reach', 'Impressions']:
        rep.setFont("Lato-Reg", 13)
        position = 110 - counter
        rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Indirect Reach' and media1 == 'Instagram':
            rep.drawString(330, position, '---')
        else:
            rep.drawString(330, position, str("{:,}".format(media_reach(
                media1, metric, followers_data, all_media, reshares))))
        rep.drawString(515, position, str("{:,}".format(media_reach(
            media2, metric, followers_data, all_media, reshares))))
        rep.drawString(700, position, str("{:,}".format(
            total_reach(metric, followers_data, all_media, reshares))))
        counter += 30
    rep.showPage()


def social_media_reach_page(rep, all_media, followers_data, reshares):
    rep.setFont('Lato-Lig', 24)
    rep.drawString(90, 543, 'SOCIAL MEDIA RESULTS')
    rep.line(80, 530, 80, 570)
    rep.rect(20, 460, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(180, 475, 'Instagram')
    rep.drawString(360, 475, 'Twitter')
    rep.drawString(520, 475, 'Facebook')
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 475, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 430 - 30 * i, 825, 430 - 30 * i)
        table_height = 430 - 30 * i
    rep.line(20, 460, 20, table_height)
    rep.line(825, 460, 825, table_height)
    rep.line(650, 460, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interactions', 'Likes/Favourites', 'Comments', 'Shares/Retweets']:
        position = 440 - counter
        if metric in ['Likes/Favourites', 'Comments', 'Shares/Retweets']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(50, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        metric = metric.split('/')[0]
        if metric == 'Shares':
            rep.setFont("Lato-Lig", 8)
            rep.drawString(190, position, '---')
        else:
            rep.drawString(180, position, str("{:,}".format(
                count_media_results('Instagram', metric, all_media))))
        rep.setFont("Lato-Lig", 13)
        if metric == 'Comments':
            rep.setFont("Lato-Lig", 8)
            rep.drawString(370, position, '---')
        else:
            rep.drawString(360, position, str("{:,}".format(
                count_media_results('Twitter', metric, all_media))))
        rep.setFont("Lato-Lig", 13)
        rep.drawString(520, position, str("{:,}".format(
            count_media_results('Facebook', metric, all_media))))
        rep.drawString(700, position, str("{:,}".format(count_media_results('Facebook', metric, all_media) + count_media_results(
            'Instagram', metric, all_media) + count_media_results('Twitter', metric, all_media))))
        counter += 30
    table_height = 0
    rep.rect(650, 280, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(685, 290, 'Average per post')
    rep.setFillColor('black')
    for i in range(5):
        rep.line(20, 280 - 30 * i, 825, 280 - 30 * i)
        table_height = 280 - 30 * i
    rep.line(20, 280, 20, table_height)
    rep.line(825, 280, 825, table_height)
    rep.line(650, 280, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Interaction Rate.Interaction per post', 'Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
        position = 260 - counter
        if metric in ['Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.setFont("Lato-Reg", 10)
            rep.drawString(50, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(50, position - 4, explain)
            rep.setFont("Lato-Reg", 13)
        else:
            explain = metric.split('.')[1]
            metric = metric.split('.')[0]
            rep.drawString(30, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(30, position - 4, explain)
            rep.setFont("Lato-Lig", 13)
        if metric == 'Amplification Rate':
            rep.setFont("Lato-Lig", 8)
            rep.drawString(190, position, '---')
        else:
            rep.setFont("Lato-Lig", 13)
            rep.drawString(180, position, str(count_media_rates('Instagram', metric, all_media)))
        rep.setFont("Lato-Lig", 13)
        if metric == 'Conversation Rate':
            rep.setFont("Lato-Lig", 8)
            rep.drawString(370, position + 4, '---')
        else:
            rep.drawString(360, position, str(count_media_rates('Twitter', metric, all_media)))
        rep.setFont("Lato-Lig", 13)
        rep.drawString(520, position, str(count_media_rates('Facebook', metric, all_media)))
        rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        counter += 30

    rep.setFillColor('black')
    table_height = 0
    rep.rect(650, 130, 175, 30, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)
    rep.drawString(700, 140, 'TOTALS')
    rep.setFillColor('black')
    for i in range(4):
        rep.line(20, 130 - 30 * i, 825, 130 - 30 * i)
        table_height = 130 - 30 * i
    rep.line(20, 130, 20, table_height)
    rep.line(825, 130, 825, table_height)
    rep.line(650, 130, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Direct Reach/Uniques', 'Indirect Reach', 'Impressions']:
        position = 110 - counter
        rep.setFont("Lato-Reg", 13)
        rep.drawString(30, position, metric)
        if '/' in metric:
            metric = metric.split('/')[0]
        rep.setFont("Lato-Lig", 13)
        if metric == 'Indirect Reach':
            rep.setFont("Lato-Lig", 8)
            rep.drawString(190, position, '---')
        else:
            rep.drawString(180, position, str("{:,}".format(media_reach(
                'Instagram', metric, followers_data, all_media, reshares))))
        rep.setFont("Lato-Lig", 13)
        if metric == 'Indirect Reach' and count_media_results('Facebook', 'Shares', all_media) != 0 and media_reach('Facebook', 'Indirect Reach', followers_data, all_media, reshares) == 0:
            rep.setFont("Lato-Lig", 8)
            rep.drawString(530, position, '---')
            rep.setFont("Lato-Lig", 13)
        else:
            rep.drawString(520, position, str("{:,}".format(media_reach(
                'Facebook', metric, followers_data, all_media, reshares))))
        rep.drawString(360, position, str("{:,}".format(media_reach(
            'Twitter', metric, followers_data, all_media, reshares))))
        rep.drawString(700, position, str("{:,}".format(
            total_reach(metric, followers_data, all_media, reshares))))
        counter += 30
    rep.showPage()


def last_page(rep):
    rep.setPageSize(landscape(A4))
    rep.setFillGray(0.1)
    rep.rect(0, 0, 900, 900, stroke=0, fill=1)
    rep.drawImage('%s/Desktop/natappy/images/last.png' % home, 0, 0, 880, 620)
    rep.showPage()


def blogger_blogposts_page(rep, dirname, blogger, blogposts, post_info):
    for blogpost in post_info[blogger]:
        layout = len(post_info[blogger][blogpost]['pieces']) * 'Aa'
        screens = post_info[blogger][blogpost]['pieces']
        with suppress(Exception):
            layouts.do_a_page(rep, blogger, screens, layout, blogpost, blogposts=True)


def pdf(all_media, tags, bloggers, fromdate, todate, dirname, platforms, followers_data, size, brandname, campaign, reshares, blogposts, post_info):
    print('Creating PDF....')
    rep = canvas.Canvas("%s/Desktop/%s/%s-%s.pdf" % (home, dirname, dirname,
                                                     str(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))), pagesize=A4)
    rep.setPageSize(landscape(A4))

  #  welcome_pages(rep,brandname,campaign)
    site_statistic_page(rep, all_media, followers_data, bloggers, platforms)
    print('Statistic page ready...')
    if len(all_media.keys()) == 3:
        social_media_reach_page(rep, all_media, followers_data, reshares)
    if len(all_media.keys()) == 2:
        two_social_media_reach_page(rep, all_media, followers_data, reshares)
    if len(all_media.keys()) == 1:
        one_social_media_reach_page(rep, all_media, followers_data, reshares)
    print('Social media results page ready...')
    if 'Instagram' in platforms:
        Instagram_results_page(rep, bloggers, all_media, followers_data)
        print('Instagram Results page ready...')
    if 'Twitter' in platforms:
        Twitter_results_page(rep, bloggers, all_media, followers_data)
        print('Twitter Results page ready...')
    if 'Facebook' in platforms:
        Facebook_results_page(rep, bloggers, all_media, followers_data)
        print('Facebook Results page ready...')

#    with suppress(Exception):
#    if size!='Quick':
#        for blogger in bloggers:
#            if post_info:
#                if blogger in blogposts:
#                    if blogposts[blogger]:
#                        blogger_blogposts_page(rep,dirname,blogger,blogposts,post_info)
#            blogger_social_media_page(rep,dirname,blogger,all_media)
#
#    last_page(rep)
    print('PDF created. Saving PDF...')
    rep.save()


# a=[562676,101217,647399,797263,730736,894473,937891,762220,527469,793082,807870,761913,1016245]

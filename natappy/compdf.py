from reportlab.pdfgen import canvas
from time import gmtime, strftime

from PIL import Image
from os.path import expanduser
import threading
from contextlib import suppress
import xlsxwriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4, landscape
import math
import layouts
import pandas

home = expanduser("~")
LOCK = threading.Lock()
platshort = {'Facebook': 'FB', 'Instagram': 'IG', 'Twitter': 'TW'}
pdfmetrics.registerFont(TTFont('Lato-Lig', 'Lato-Lig.ttf'))
pdfmetrics.registerFont(TTFont('Lato-Reg', 'Lato-Reg.ttf'))


def screenname_to_linkname(blogger, media):
    try:
        a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
        b = pandas.DataFrame(a)
        return list(b[b['Blogger'] == blogger][media])[0]
    except:
        return 'Natalia'


def linkname_to_screenname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b[media] == blogger]['Blogger'])[0]


def find_screenshots(dirname, all_media):
    screenshots_paths = {}
    for media in all_media.keys():
        for post in all_media[media].keys():
            post_path = '%s/Desktop/%s/%s_screenshots/%s.png' % (home, dirname, media, all_media[media][post][
                                                                 'authortw'] + '_' + all_media[media][post]['post_id'])
            img = Image.open(post_path)
            ratio = img.size[0] / img.size[1]
            if ratio <= 1:
                position = 'portrait'
            if ratio > 1:
                position = 'landscape'
            screenshots_paths[post_path] = {'width': img.size[
                0], 'height': img.size[1], 'position': position}
    return screenshots_paths


def other_social_media_page(rep, bloggers, dirname, all_media):
    screens = find_other_screenshots(dirname, bloggers, all_media)
    pages = choose_screenshots_layout(screens)
    for page in pages.keys():
        layout = page_layout(pages[page])[0]
        screens = page_layout(pages[page])[1]
        try:
            layouts.do_a_page(rep, 'Competition Entries', screens, layout)
        except:
            pass


def find_other_screenshots(dirname, bloggers, all_media):
    screenshots_paths = {}
    for media in all_media.keys():
        for post in all_media[media].keys():
            post_path = '%s/Desktop/%s/%s_screenshots/%s.png' % (home, dirname, media, all_media[media][post][
                                                                 'authortw'] + '_' + str(all_media[media][post]['post_id']))
            try:
                img = Image.open(post_path)
            except:
                post_path = '%s/Desktop/%s/%s_screenshots/%s.png' % (
                    home, dirname, media, str(all_media[media][post]['post_id']))
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


def social_media_page(rep, dirname, all_media, blogger=''):
    screens = find_screenshots(dirname, all_media)
    pages = choose_screenshots_layout(screens)
    for page in pages.keys():
        layout = page_layout(pages[page])[0]
        screens = page_layout(pages[page])[1]
        try:
            layouts.do_a_page(rep, screens, layout)
        except:
            pass


def stringWidth2(string, font='Lato-Lig', size=24, charspace=0):
    width = stringWidth(string, 'Lato-Lig', 24)
    width += (len(string) - 1) * charspace
    return width


def welcome_pages(rep, brandname, campaign):
    rep.drawImage('%s/Desktop/natappy/images/first.png' %
                  home, 250, 280, 400, 300)  # 260,320,300,100
    rep.setFont('Lato-Lig', 24)
    brandname = ' '.join([letter.upper() for letter in brandname])
    brand_position = 421 - stringWidth2(brandname, font='Lato-Lig', size=24, charspace=0) / 2
    campaign = ' '.join([letter.upper() for letter in campaign])
    campaign_position = 421 - stringWidth2(campaign, font='Lato-Lig', size=24, charspace=0) / 2
    rep.drawString(brand_position, 250, brandname)
    rep.drawString(campaign_position, 190, campaign)
    rep.drawString(240, 130, "P O S T  C A M P A I G N  R E P O R T")
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


def media_posts_count(media, all_media):
    return int(len(all_media[media].keys()))


def media_likes_count(media, all_media):
    return sum([all_media[media][post]['likes'] for post in all_media[media]])


def media_comments_count(media, all_media):
    return sum([all_media[media][post]['comments'] for post in all_media[media]])


def media_shares_count(media, all_media):
    return sum([all_media[media][post]['shares'] for post in all_media[media]])


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
    if metric == 'Interaction':
        return media_interactions_count(media, all_media)


def count_media_rates(media, metric, all_media):
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
    if metric == 'Interactions Rate':
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
    if metric == 'Interactions Rate':
        with suppress(Exception):
            rate = sum([media_interactions_count(media, all_media) for media in all_media.keys()]
                       ) / sum([media_posts_count(media, all_media) for media in all_media.keys()])
            return str(("%.2f" % rate))
    return toreturn


def count_media_impression(all_media, media, followers_data):
    media_impression = 0
    for post in all_media[media]:
        media_impression += all_media[media][post]['followers']
    return media_impression


def media_reach(media, metric, followers_data, all_media):
    if metric == 'Direct Reach':
        return count_media_impression(all_media, media, followers_data)
    if metric == 'Impression':
        return count_media_impression(all_media, media, followers_data)


def total_reach(metric, followers_data, all_media):
    if metric == 'Direct Reach':
        return sum([count_media_impression(all_media, media, followers_data) for media in all_media.keys()])
    if metric == 'Impression':
        return sum([count_media_impression(all_media, media, followers_data) for media in all_media.keys()])


def two_social_media_reach_page(rep, all_media, followers_data):
    media1 = 'Instagram' if 'Instagram' in all_media.keys() else 'Twitter'
    media2 = [media for media in list(all_media.keys()) if media != media1][0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(150, 500, 'SOCIAL MEDIA COMPETITION ENTRIES RESULTS')
    rep.line(130, 490, 750, 490)
    rep.rect(20, 420, 805, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(310, 435, media1)
    rep.drawString(545, 435, media2)
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 435, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interaction', 'Likes/Favourites', 'Comments', 'Shares/Retweets']:
        position = 400 - counter
        if metric in ['Likes/Favourites', 'Comments', 'Shares/Retweets']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        metric = metric.split('/')[0]
        if metric == 'Shares':
            rep.drawString(330, position, '---')
            rep.drawString(565, position, str("{:,}".format(
                count_media_results(media2, 'Shares', all_media))))
        if metric == 'Comments':
            rep.drawString(565, position, '---')
            rep.drawString(330, position, str("{:,}".format(
                count_media_results(media1, 'Comments', all_media))))
        if metric in ['Posts', 'Interaction', 'Likes']:
            metric = metric.split('/')[0]
            rep.drawString(330, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
            rep.drawString(565, position, str("{:,}".format(
                count_media_results(media2, metric, all_media))))
        rep.drawString(700, position, str("{:,}".format(count_media_results(
            media1, metric, all_media) + count_media_results(media2, metric, all_media))))
        counter += 30
    table_height = 0
    for i in range(5):
        rep.line(20, 230 - 30 * i, 825, 230 - 30 * i)
        table_height = 230 - 30 * i
    rep.line(20, 230, 20, table_height)
    rep.line(825, 230, 825, table_height)
    rep.line(650, 230, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 10)
    for metric in ['Interactions Rate.Interaction per post', 'Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
        position = 210 - counter
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
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(30, position - 4, metric)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Conversation Rate':
            rep.drawString(565, position, '---')
            rep.drawString(330, position, str(count_media_rates(
                media1, 'Conversation Rate', all_media)))
        if metric == 'Amplification Rate':
            rep.drawString(330, position, '---')
            rep.drawString(565, position, str(count_media_rates(
                media2, 'Amplification Rate', all_media)))
        if metric in ['Interactions Rate', 'Applause Rate']:
            metric = metric.split('.')[0]
            rep.drawString(330, position, str(count_media_rates(media1, metric, all_media)))
            rep.drawString(565, position, str(count_media_rates(media2, metric, all_media)))
        metric = metric.split('.')[0]
        rep.drawString(700, position, str(count_total_rates(metric, all_media)))
        counter += 30
    rep.rect(650, 230, 175, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 12)
    rep.drawString(690, 247, 'Average per post')
    rep.setFillColor('black')
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    table_height = 0
    rep.rect(650, 70, 175, 40, fill=1)
    rep.setFillColor('white')
    rep.drawString(700, 85, 'TOTALS')
    rep.setFillColor('black')
    for i in range(2):
        rep.line(20, 70 - 30 * i, 825, 70 - 30 * i)
        table_height = 70 - 30 * i
    rep.line(20, 70, 20, table_height)
    rep.line(825, 70, 825, table_height)
    rep.line(650, 70, 650, table_height)
    counter = 0
    for metric in ['Impression']:
        position = 50 - counter
        rep.setFont("Lato-Reg", 13)
        rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        rep.drawString(330, position, str("{:,}".format(
            media_reach(media1, metric, followers_data, all_media))))
        rep.drawString(565, position, str("{:,}".format(
            media_reach(media2, metric, followers_data, all_media))))
        rep.drawString(700, position, str("{:,}".format(
            total_reach(metric, followers_data, all_media))))
        counter += 30
    rep.showPage()


def one_social_media_reach_page(rep, all_media, followers_data):
    media1 = list(all_media.keys())[0]
    rep.setFont('Lato-Lig', 24)
    rep.drawString(150, 500, 'SOCIAL MEDIA COMPETITION ENTRIES RESULTS')
    rep.line(130, 490, 750, 490)
    rep.rect(20, 420, 805, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 13)
    rep.drawString(455, 435, media1)
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 435, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interaction', 'Likes/Favourites', 'Comments', 'Shares/Retweets']:
        position = 400 - counter
        if metric in ['Likes/Favourites', 'Comments', 'Shares/Retweets']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        metric = metric.split('/')[0]
        if metric == 'Shares':
            if media1 == 'Instagram':
                rep.drawString(465, position, '---')
                rep.drawString(720, position, '---')
            else:
                rep.drawString(465, position, str("{:,}".format(
                    count_media_results(media1, 'Shares', all_media))))
                rep.drawString(720, position, str("{:,}".format(
                    count_media_results(media1, 'Shares', all_media))))
        if metric == 'Comments':
            if media1 == 'Twitter':
                rep.drawString(465, position, '---')
                rep.drawString(720, position, '---')
            else:
                rep.drawString(465, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
                rep.drawString(720, position, str("{:,}".format(
                    count_media_results(media1, 'Comments', all_media))))
        if metric in ['Posts', 'Interaction', 'Likes']:
            metric = metric.split('/')[0]
            rep.drawString(465, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
            rep.drawString(720, position, str("{:,}".format(
                count_media_results(media1, metric, all_media))))
        counter += 30
    table_height = 0
    for i in range(5):
        rep.line(20, 230 - 30 * i, 825, 230 - 30 * i)
        table_height = 230 - 30 * i
    rep.line(20, 230, 20, table_height)
    rep.line(825, 230, 825, table_height)
    rep.line(650, 230, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 10)
    for metric in ['Interactions Rate.Interaction per post', 'Applause Rate.Likes per post', 'Conversation Rate.Comments per post', 'Amplification Rate.Shares per post']:
        position = 210 - counter
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
            rep.setFont("Lato-Reg", 13)
            rep.drawString(30, position + 4, metric)
            rep.setFont("Lato-Lig", 7)
            rep.drawString(30, position - 4, metric)
        rep.setFont("Lato-Lig", 13)
        if metric == 'Conversation Rate':
            if media1 == 'Twitter':
                rep.drawString(465, position, '---')
                rep.drawString(720, position, '---')
            else:
                rep.drawString(465, position, str(count_media_rates(
                    media1, 'Conversation Rate', all_media)))
                rep.drawString(720, position, str(
                    count_total_rates('Conversation Rate', all_media)))
        if metric == 'Amplification Rate':
            if media1 == 'Instagram':
                rep.drawString(465, position, '---')
                rep.drawString(720, position, '---')
            else:
                rep.drawString(465, position, str(count_media_rates(
                    media1, 'Amplification Rate', all_media)))
                rep.drawString(720, position, str(
                    count_total_rates('Amplification Rate', all_media)))
        if metric in ['Interactions Rate', 'Applause Rate']:
            rep.drawString(465, position, str(count_media_rates(media1, metric, all_media)))
            rep.drawString(720, position, str(count_total_rates(metric, all_media)))
        counter += 30
    rep.rect(650, 230, 175, 40, fill=1)
    rep.setFillColor('white')
    rep.setFont("Lato-Reg", 12)
    rep.drawString(690, 247, 'Average per post')
    rep.setFillColor('black')
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    table_height = 0
    rep.rect(650, 70, 175, 40, fill=1)
    rep.setFillColor('white')
    rep.drawString(700, 85, 'TOTALS')
    rep.setFillColor('black')
    for i in range(2):
        rep.line(20, 70 - 30 * i, 825, 70 - 30 * i)
        table_height = 70 - 30 * i
    rep.line(20, 70, 20, table_height)
    rep.line(825, 70, 825, table_height)
    rep.line(650, 70, 650, table_height)
    counter = 0
    for metric in ['Impression']:
        position = 50 - counter
        rep.setFont("Lato-Reg", 13)
        rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        rep.drawString(465, position, str("{:,}".format(
            media_reach(media1, metric, followers_data, all_media))))
        rep.drawString(720, position, str("{:,}".format(
            total_reach(metric, followers_data, all_media))))
        counter += 30
    rep.showPage()


def social_media_reach_page(rep, all_media, followers_data):
    rep.setFont('Lato-Lig', 24)
    media1, media2, media3 = 'Instagram', 'Twitter', 'Facebook'
    rep.drawString(150, 500, 'SOCIAL MEDIA COMPETITION ENTRIES RESULTS')
    rep.line(130, 490, 750, 490)
    rep.rect(20, 420, 805, 40, fill=1)
    rep.setFillColor('white')  # choose your font colour
    rep.setFont("Lato-Reg", 13)  # choose your font type and font size
    rep.drawString(230, 435, media1)
    rep.drawString(410, 435, media2)
    rep.drawString(570, 435, media3)
    rep.setFont("Lato-Reg", 17)
    rep.drawString(700, 435, 'TOTALS')
    table_height = 0
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Posts', 'Interaction', 'Likes', 'Comments', 'Shares']:
        position = 400 - counter
        if metric in ['Likes', 'Comments', 'Shares']:
            rep.setFont("Lato-Ret", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Reg", 13)
        rep.drawString(240, position, str("{:,}".format(
            count_media_results(media1, metric, all_media))))
        rep.drawString(420, position, str("{:,}".format(
            count_media_results(media2, metric, all_media))))
        rep.drawString(580, position, str("{:,}".format(
            count_media_results(media3, metric, all_media))))
        rep.drawString(710, position, str("{:,}".format(count_media_results('Facebook', metric, all_media) + count_media_results(
            'Instagram', metric, all_media) + count_media_results('Twitter', metric, all_media))))
        counter += 30
    table_height = 0
    for i in range(5):
        rep.line(20, 230 - 30 * i, 825, 230 - 30 * i)
        table_height = 230 - 30 * i
    rep.line(20, 230, 20, table_height)
    rep.line(825, 230, 825, table_height)
    rep.line(650, 230, 650, table_height)
    counter = 0
    rep.setFont("Lato-Reg", 13)
    for metric in ['Interactions Rate', 'Applause Rate', 'Conversation Rate', 'Amplification Rate']:
        position = 210 - counter
        if metric in ['Applause Rate', 'Conversation Rate', 'Amplification Rate']:
            rep.setFont("Lato-Reg", 10)
            rep.drawString(55, position, metric)
            rep.setFont("Lato-Reg", 13)
        else:
            rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        rep.drawString(240, position, str(count_media_rates(media1, metric, all_media)))
        rep.drawString(420, position, str(count_media_rates(media2, metric, all_media)))
        rep.drawString(580, position, str(count_media_rates(media3, metric, all_media)))
        rep.drawString(710, position, str(count_total_rates(metric, all_media)))
        counter += 30
    for i in range(5):
        rep.line(20, 390 - 30 * i, 825, 390 - 30 * i)
        table_height = 390 - 30 * i
    rep.line(20, 420, 20, table_height)
    rep.line(825, 420, 825, table_height)
    rep.line(650, 420, 650, table_height)
    rep.setFillColor('black')
    table_height = 0
    for i in range(2):
        rep.line(20, 70 - 30 * i, 825, 70 - 30 * i)
        table_height = 70 - 30 * i
    rep.line(20, 70, 20, table_height)
    rep.line(825, 70, 825, table_height)
    rep.line(650, 70, 650, table_height)
    counter = 0
    for metric in ['Impression']:
        rep.setFont("Lato-Reg", 13)
        position = 50 - counter
        rep.drawString(30, position, metric)
        rep.setFont("Lato-Lig", 13)
        rep.drawString(240, position, str("{:,}".format(
            media_reach(media1, metric, followers_data, all_media))))
        rep.drawString(420, position, str("{:,}".format(
            media_reach(media2, metric, followers_data, all_media))))
        rep.drawString(580, position, str("{:,}".format(
            media_reach(media3, metric, followers_data, all_media))))
        rep.drawString(710, position, str("{:,}".format(
            total_reach(metric, followers_data, all_media))))
        counter += 30
    rep.showPage()


def last_page(rep):
    rep.setPageSize(landscape(A4))
    rep.setFillGray(0.1)
    rep.rect(0, 0, 900, 900, stroke=0, fill=1)
    rep.drawImage('%s/Desktop/natappy/images/last.png' % home, 0, 0, 830, 595)
    rep.showPage()


def select_bloggers_posts(all_media, bloggers):
    selected_posts = {}
    for media in all_media.keys():
        selected_posts[media] = {}
        for post in all_media[media].keys():
            if all_media[media][post]['authortw'] in [screenname_to_linkname(blogger, media) for blogger in bloggers]:
                selected_posts[media][post] = all_media[media][post]
    return selected_posts


def select_others_posts(all_media, bloggers):
    selected_posts = {}
    for media in all_media.keys():
        selected_posts[media] = {}
        for post in all_media[media].keys():
            if all_media[media][post]['authortw'] not in [screenname_to_linkname(blogger, media) for blogger in bloggers]:
                selected_posts[media][post] = all_media[media][post]
    return selected_posts


def pdf(all_media, dirname, bloggers, tags, fromdate, platforms, followers_data, brandname, campaign):
    print('Creating PDF....')
    rep = canvas.Canvas("%s/Desktop/%s/%s-%s.pdf" % (home, dirname, dirname,
                                                     str(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))), pagesize=A4)
    rep.setPageSize(landscape(A4))
    welcome_pages(rep, brandname, campaign)
    all_media = select_others_posts(all_media, bloggers)
    if len(all_media.keys()) == 3:
        social_media_reach_page(rep, all_media, followers_data)
    if len(all_media.keys()) == 2:
        two_social_media_reach_page(rep, all_media, followers_data)
    if len(all_media.keys()) == 1:
        one_social_media_reach_page(rep, all_media, followers_data)
    print('Social media results page ready...')
    other_social_media_page(rep, bloggers, dirname, all_media)
    last_page(rep)
    print('PDF done!!!')
    rep.save()


def count_media_followers(all_media, media):
    return sum([all_media[media][post]['followers'] for post in all_media[media].keys()])


def excel_format(all_media, followers_data):
    tweets_to_excel = []
    for media in all_media:
        for post in all_media[media]:
            tweet_details = [all_media[media][post]['media'], count_media_followers(all_media, media),
                             all_media[media][post]['author'], all_media[media][post]['followers'], str(all_media[media][post]['post_id']), all_media[media][post]['text'], all_media[media][post]['created_at'], all_media[media][post]['link'], all_media[media][post]['likes'], all_media[media][post]['comments'], all_media[media][post]['shares'], all_media[media][post]['engagement']]
            tweets_to_excel.append(tweet_details)
    return tweets_to_excel


def excel(dirname, our_posts, followers_data):
    print('Creating excel....')
    workbook = xlsxwriter.Workbook('%s/Desktop/%s/competition.xlsx' % (home, dirname))
    worksheet = workbook.add_worksheet()
    fieldsnames = ('MEDIA', 'IMPRESSION', 'AUTHOR', 'AUTHOR_FOLLOWERS', 'POST_ID',
                   'TEXT', 'CREATED_AT', 'LINK', 'LIKES', 'COMMENTS', 'SHARES', 'ENGAGEMENT')
    for col, name in enumerate(fieldsnames):
        worksheet.write(0, col, name)
    posts = excel_format(our_posts, followers_data)
    for row, post in enumerate(posts, 1):
        for col, name in enumerate(post):
            try:
                worksheet.write(row, col, name)
            except:
                pass
    workbook.close()

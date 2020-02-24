import requests
import time
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
c=0
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
#Getting the soucrce code
site_url = "http://www.snooker.org"
main_url = requests.get(site_url,headers = headers)
main_soup = BeautifulSoup(main_url.content,'html.parser')
main_div = main_soup.find('div',{'class':'artikkel'})
main_links=[]
tournament_name = main_div.h2.text
#GETTING ADDRESSES


choice=0

while choice>=0:
    
    for i in main_div.find_all('a'):
        main_links.append(i['href'])
        #if c==2:
         #   break
        #c+=1***
    live_link = site_url + main_links[0]
    result_link = site_url + main_links[1]
    upcoming_link = site_url + main_links[2]
    player_list_left = []
    player_list_right = []
    score_str = []
    rounds = []

    
    #Menu
    if choice == 0:
        i=0
        player_list_left = []
        player_list_right = []
        score_str = []
        rounds = []
        
        print()
        print('                   '+tournament_name)
        print()
        print('0.Referesh')
        print('1.Live Scores')
        print('2.Results')
        print('3.Upcoming Matches')
        print('-1.EXIT')
        choice=int(input('ENTER YOUR CHOICE:'))
        
    #LIVE    
    if choice == 1:
        live_url = requests.get(live_link,headers = headers)
        live_soup = BeautifulSoup(live_url.content,'html.parser')
        tr_player = live_soup.find_all("tr",{"class":"multiple"})
        i=0
        framewise_link = []
        live_coverage_link = []
        for row in tr_player:

            #EXCTRACTING ROUND

            this_round = row.find('td',{'class':'round'})
            round_text = this_round.find('a')
            rounds.append(re.sub(r'[^\w]',' ',round_text.text))
            
            #EXTRACTING FRAMEWISE LINKS
            
            framewise_link.append(row.find('a',{'class':'scores'})['href'])
            
            
            
            
            #EXTRACTING NAMES

            name_box = row.find_all('td',{'class':'player'})
            for name in name_box:
                link = name.find('a')
                if(link is None):
                    break
                name_text = re.sub(r'[^\w]',' ',link.text)
                if not name_text:
                    break
                if i % 2 == 0:
                    player_list_left.append(name_text)
                else:
                    player_list_right.append(name_text)
                i+=1

            #EXTRACTING SCORES

            score_left = row.find('td',{'class':'first-score'})
            score_right = row.find('td',{'class':'last-score'})
            score_str.append(re.sub(r'[^\w]',' ',score_left.text)+'-'+re.sub(r'[^\w]',' ',score_right.text))
            

            #EXTRACTING LIVE COVERAGE LINKS
            
            live_coverage_link.append(row.find('a',{'title':'Shot-by-shot coverage from World Snooker'})['href'])
            
            
        
        table = PrettyTable(['Match No.','ROUND','PLAYER1','SCORE','PLAYER2'])
        for x in range(0,len(player_list_left)):
            table.add_row([len(player_list_left)-x,rounds[x],player_list_left[x],score_str[x],player_list_right[x]])

        print()
        print('                   '+tournament_name)
        print()
        print(table)
        print()

                
        print('0.Back')
        print('1.Referesh')
        print('2.Match details')
        print('-1.EXIT')
        inner_choice=int(input('Enter your choice:'))
        if inner_choice == 2:
            inner_choice = 2
            n=int(input('Enter the match no for framewise scores:'))
            while(inner_choice==2):
                k=0
                pdl = []
                pdr = []
                l = 0
                c = 0
                r = 0
                
                detail_url = requests.get(framewise_link[len(player_list_left)-n])
                detail_soup = BeautifulSoup(detail_url.content,'html.parser')
                for i in detail_soup.find_all('p',{'class':'name'}):
                    if k%2==1:
                        pdr.append(i.a.text)
                    else:
                        pdl.append(i.a.text)
                        k+=1
                pdl.append(detail_soup.find('p',{'class':'score score-player1 text-right'}).text)
                pdr.append(detail_soup.find('p',{'class':'score score-player2'}).text)
                pdl.append(detail_soup.find('p',{'class':'score score-player1 score-ast score-ast-left text-right'}).text)
                pdr.append(detail_soup.find('p',{'class':'score score-player2 score-ast'}).text)
                detail_table = PrettyTable(['  ',pdl[0],'Vs',pdr[0],' '])
                detail_table.add_row([' ',pdl[1],detail_soup.find('p',{'class':'frames text-center'}).text,pdr[1],'  '])
                detail_table.add_row(['  ',pdl[2],'AST',pdr[2],' '])
                detail_table.add_row(['Breaks(50+) ',' Points','#','Points ',' Breaks(50+)'])
                score_table = detail_soup.find('table',{'class','table table-responsive frame-data'})
                #print(score_table)
                for tr in score_table.tbody.find_all('tr'):
                    score_row = []
                    for td in tr.find_all('td'):
                        score_row.append(td.text)
                    if int(score_row[3]) > int(score_row[1]):
                        r+=1
                    else:
                        l+=1
                    c+=1
                    score_row[2] = "{} ({}-{})".format(c,l,r)
                    detail_table.add_row(score_row)

                print(detail_table)
                print()
                print('0.Back')
                print('1.Live Coverage(DONT SELECT)')
                print('2.Referesh')
                print('-1.EXIT')
                inner_choice=int(input('Enter your choice:'))
                
                if inner_choice == 1:
                    while(True):
                        z=0
                        live_scores = []
                        cover_link = requests.get(live_coverage_link[len(player_list_left)-n])
                        cover_soup = BeautifulSoup(cover_link.content,'html.parser')
                        l_name = cover_soup.find('span',{'class':'live-match-val-player1'}).text
                        r_name = cover_soup.find('span',{'class':'live-match-val-player2'}).text
                        main_score_div = cover_soup.find_all('div',{'class':'col-lg-4 col-md-4 col-sm-4 col-xs-4'})

                        live_rows = main_score_div[1].find_all('tr')
                        for i in live_rows:
                            if z % 2 == 0:
                                td = i.find_all('td')
                                for j in td:
                                    live_scores.append(j.text)
                        z+=1
                        live_table = PrettyTable([l_name,'Vs',r_name])
                        live_table.add_row([live_scores[0],'Frames',live_scores[1]])
                        live_table.add_row(['  ',live_scores[2],' '])
                        live_table.add_row([live_scores[3],'Points',live_scores[4]])
                        live_table.add_row(['  ',live_scores[5],' '])
                        live_table.add_row([live_scores[6],'Break',live_scores[7]])

                        print(live_table)


                        #inner_choice = int(input("Enter your choice:"))
                        time.sleep(23)
                        
                if inner_choice == 0:
                    inner_choice = 1
            
        choice = inner_choice
            

    #Results
    if choice == 2:
        framewise_link = []
        result_url = requests.get(result_link)
        result_soup = BeautifulSoup(result_url.content,'html.parser')
        table = result_soup.find("table",{"class":"display matches"})

        tr_player = table.find_all("tr",{"class":"gradeA"})
        i=0
        for row in tr_player:

            #EXCTRACTING ROUND

            this_round = row.find('td',{'class':'round'})
            round_text = this_round.find('a')
            rounds.append(re.sub(r'[^\w]',' ',round_text.text))
            
            #EXTRACTING FRAMEWISE LINKS
            
            framewise_link.append(row.find('a',{'class':'scores'})['href'])
            
            #EXTRACTING NAMES

            name_box = row.find_all('td',{'class':'player'})
            for name in name_box:
                link = name.find('a')
                if(link is None):
                    break
                name_text = re.sub(r'[^\w]',' ',link.text)
                if not name_text:
                    break
                if i % 2 == 0:
                    player_list_left.append(name_text)
                else:
                    player_list_right.append(name_text)
                i+=1

            #EXTRACTING SCORES

            score_left = row.find('td',{'class':'first-score'})
            score_right = row.find('td',{'class':'last-score'})
            score_str.append(re.sub(r'[^\w]',' ',score_left.text)+'-'+re.sub(r'[^\w]',' ',score_right.text))
            

            
            
        
        table = PrettyTable(['Match No.','ROUND','WINNER','SCORE','LOSER'])
        for x in range(0,len(player_list_left)):
            table.add_row([len(player_list_left)-x,rounds[x],player_list_left[x],score_str[x],player_list_right[x]])

        print()
        print('                   '+tournament_name)
        print()
        print(table)
        print()
        print('0.Back')
        print('1.Match Details')
        print('-1.EXIT')
        choice=int(input('Enter your choice:'))
        if choice == 1:
            inner_choice = 1
            while(inner_choice==1):
                k=0
                pdl = []
                pdr = []
                l = 0
                c = 0
                r = 0
                n=int(input('Enter the match no for framewise scores:'))
                detail_url = requests.get(framewise_link[len(player_list_left)-n])
                detail_soup = BeautifulSoup(detail_url.content,'html.parser')
                for i in detail_soup.find_all('p',{'class':'name'}):
                    if k%2==1:
                        pdr.append(i.a.text)
                    else:
                        pdl.append(i.a.text)
                        k+=1
                pdl.append(detail_soup.find('p',{'class':'score score-player1 text-right'}).text)
                pdr.append(detail_soup.find('p',{'class':'score score-player2'}).text)
                pdl.append(detail_soup.find('p',{'class':'score score-player1 score-ast score-ast-left text-right'}).text)
                pdr.append(detail_soup.find('p',{'class':'score score-player2 score-ast'}).text)
                detail_table = PrettyTable(['  ',pdl[0],'Vs',pdr[0],' '])
                detail_table.add_row([' ',pdl[1],detail_soup.find('p',{'class':'frames text-center'}).text,pdr[1],'  '])
                detail_table.add_row(['  ',pdl[2],'AST',pdr[2],' '])
                detail_table.add_row(['Breaks(50+) ',' Points','#','Points ',' Breaks(50+)'])
                score_table = detail_soup.find('table',{'class','table table-responsive frame-data'})
                #print(score_table)
                for tr in score_table.tbody.find_all('tr'):
                    score_row = []
                    for td in tr.find_all('td'):
                        score_row.append(td.text)
                    if int(score_row[3]) > int(score_row[1]):
                        r+=1
                    else:
                        l+=1
                    c+=1
                    score_row[2] = "{} ({}-{})".format(c,l,r)
                    detail_table.add_row(score_row)

                print(detail_table)
                print()
                print('0.Back')
                print('1.Match Details')
                print('-1.EXIT')
                inner_choice=int(input('Enter your choice:'))
            
            choice = inner_choice

                
            
    #Upcoming matches    
    elif choice == 3:
        upcoming_url = requests.get(upcoming_link)
        upcoming_soup = BeautifulSoup(upcoming_url.content,'html.parser')
        schedule = []
        
        if (upcoming_soup.find("table",{"class":"display matches"}) is None):
            print()
            print("***No Upcoming Matches Registered For This Event***")
        else:
            table = upcoming_soup.find("table",{"class":"display matches"})
            tr_player = table.find_all("tr",{"class":"gradeA"})
            for row in tr_player:

                #EXCTRACTING ROUND

                this_round = row.find('td',{'class':'round'})
                round_text = this_round.find('a')
                rounds.append(re.sub(r'[^\w]',' ',round_text.text))

                #EXTRACTING NAMES

                name_box = row.find_all('td',{'class':'player'})
                for name in name_box:
                    link = name.find('a')
                    if(link is None):
                        break
                    name_text = re.sub(r'[^\w]',' ',link.text)
                    if not name_text:
                        break
                    if i % 2 == 0:
                        player_list_left.append(name_text)
                    else:
                        player_list_right.append(name_text)
                    i+=1

                schedule_text = row.find('td',{'class':'scheduled editcell'}).text
                schedule.append(schedule_text)

            print()
            print('                   '+tournament_name)

            table = PrettyTable(['ROUND','PLAYER1','PLAYER2','SCHEDULE'])
            for x in range(0,len(player_list_left)):
                table.add_row([rounds[x],player_list_left[x],player_list_right[x],schedule[x]])

            print()
            print(table)
        print()
        print('0.Back')
        print('-1.EXIT')
        choice=int(input('Enter your choice:'))
        
print()
print("**TERMINATED**")


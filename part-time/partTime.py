import os
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from read_config import read_config

def load_processed_jobs(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set()

def save_processed_jobs(file_path, jobs):
    with open(file_path, 'a', encoding='utf-8') as f:
        for job in jobs:
            f.write(job + '\n')

def main():
    url = "https://www.ptt.cc/bbs/part-time/index.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.select('div.r-ent div.title')

    processed_jobs_file = 'processed_jobs.txt'
    processed_jobs = load_processed_jobs(processed_jobs_file)

    new_jobs = []

    for title in titles:
        clean_title = title.text.strip()  # 去除多餘的換行符號與空白
        if any(keyword in clean_title for keyword in keywords) and '已徵到' not in clean_title:
            job_entry = clean_title + ': https://www.ptt.cc' + title.a['href']
            if job_entry not in processed_jobs:
                new_jobs.append(job_entry)

    save_processed_jobs(processed_jobs_file, new_jobs)
    return new_jobs

if __name__ == '__main__':
    keywords = ['高雄', '鳳山']

    jobs = main()

    webhook_url = read_config('discord', 'webhook_url')

    webhook = DiscordWebhook(webhook_url, username='Part Time工作機會')
    
    if jobs != []:
        embed = DiscordEmbed(title='新工作機會!!!')
        for i, job in enumerate(jobs):
            embed.add_embed_field(name=f'工作{i+1}', value=job, inline=False)
        webhook.add_embed(embed)
        webhook.execute()
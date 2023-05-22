import asyncio
import httpx
import re
import os
from tqdm import tqdm


video_url = input("Введите url видео: ")
file_id = re.search('videos/(.+)', video_url).group(1)
segment_uri_template = video_url + '/segment-{segment_id}-sHD-v1-a1.ts'

headers = {
    "Referer": video_url,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}

def check_segment(segment_id):
    return httpx.head(
        segment_uri_template.format(video_id='55111_NePHiLSAi0133prd', segment_id=segment_id), 
        headers=headers,
    ).status_code == 200

async def get_segment(client, segment_id):
    for i in range(3):
        try:
            return (await client.get(
                segment_uri_template.format(video_id='55111_NePHiLSAi0133prd', segment_id=segment_id), 
                headers=headers,
                timeout=9999,
            )).content
        except:
            pass

left = 0
right = 32768
video_length = (right + left) // 2

print("Определяем длину видео...")
while right - left > 1:
    if not check_segment(video_length):
        right = video_length
    else:
        left = video_length

    video_length = (right + left) // 2


temp_file_name = f'umschool_{file_id}.not_ready'
final_file_name =  f'umschool_{file_id}.mp4'


async def main():
    file = open(temp_file_name, 'wb')

    async with httpx.AsyncClient() as client:
        tasks = {
            seg: asyncio.ensure_future(get_segment(client, seg + 1)) for seg in range(video_length)
        }

        for seg in tqdm(range(video_length)):
            if not tasks[seg].done():
                await asyncio.sleep(5)
                continue
            file.write(tasks[seg].result())
            tasks.pop(seg)

    file.close()

    print("Завершение...")
    os.rename(temp_file_name, final_file_name)

if __name__ == '__main__':
    asyncio.run(main())

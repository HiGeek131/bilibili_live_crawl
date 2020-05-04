# coding:utf-8
import ffmpy3
import requests
import time
import sys

uid = 4893237


def download_video(video_url, file_name):
    ff = ffmpy3.FFmpeg(inputs={video_url: '-headers "User-Agent: (Windows NT 10.0; WOW64) PotPlayer/1.7.18495" -y'},
                       outputs={file_name + str(uid) + time.strftime('%Y-%m-%d-%H-%M-%S') + '.flv': '-c copy'})
    print(ff.cmd)
    ff.run()


def get_live_info(user_id):
    r = requests.get('https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld', params={'mid': user_id})
    return r.json()


def get_video_url(room_id):
    r = requests.get('https://api.live.bilibili.com/room/v1/Room/playUrl', params={'cid': room_id, 'qn': 10000})
    res_list = r.json()
    return res_list['data']['durl'][0]['url']


def is_live(res_list):
    if res_list['data']['liveStatus'] == 1:
        room_name = res_list['data']['title']
        room_id = res_list['data']['roomid']

        print('开播了!')
        print('房间名为：' + room_name)
        print('房间号为：%d' % room_id)

        video_url = get_video_url(room_id)
        download_video(video_url, room_name)
    else:
        print('未开播！')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('没有输入UID，将以默认UID 4893237（HiGeek工作室）执行')
    elif len(sys.argv) == 2:
        print('将以UID %d 执行' % uid)
        uid = sys.argv[1]
    else:
        print('输入参数过多！')
    while True:
        live_info = get_live_info(uid)
        is_live(live_info)
        time.sleep(10)

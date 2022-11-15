#웹소켓 서버 코드

import asyncio
import websockets
import time

import serial

from datetime import datetime

#arduino
ser = serial.Serial(
    port='COM3',
    baudrate=9600)



# 보내기
async def looper(websocket):
    while True:
        # 아두이노 데이터 읽어오기py
        data = ser.read_all()
        t = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        data = str(data, 'utf-8')
        data = data.split(' ')
        # print(data)

        # 데이터가 들어온다면
        if data != ['']:
            #온습도 데이터를 각각 변수에 저장
            hum = data[1]
            tem = data[3]
            send_data = str(hum) + ','+ str(tem) + ',' + str(t)
            print(hum, tem)
            await websocket.send(send_data)
            # await websocket.send(''.join(tem))

        # 아예 슬립을 안주면 출력이 처리속도를 못따라가는지 서버 접속을 끊은 후에야 클라이언트에 몰아서 출력됨 -> 따라서 딜레이를 조금이라도 줘야하는 듯
        await asyncio.sleep(2)


async def arduino(websocket):
    future = asyncio.ensure_future(looper(websocket))
    #정해준 time동안 계속 실행
    await asyncio.sleep(10000)



async def main():
    #localhost:8765 주소에 웹소켓 서버를 실행
    async with websockets.serve(arduino, "localhost",8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
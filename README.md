# discordpy-example
discord.py rewrite 버전으로 제작된 간단한 한국어 디스코드 챗봇입니다.
on_message 이벤트가 아닌, 데코레이터(discord.ext 모듈)를 사용하여 명령어를 제작하였습니다.


# 사용 범위
본 코드는 MIT 라이센스를 따릅니다.
상업적인 용도로도 자유롭게 이용이 가능하며, 수정, 2차 배포가 가능합니다.
단, 사용하실 때 반드시 해당 깃허브 리포지토리 링크를 기재하여 주시기 바랍니다.


# 사용 방법
https://python.org 에서 Python을 설치합니다.
설치할 때 PATH에 체크하시면 모듈을 설치할 때 더욱 편합니다.

CMD를 열어 `pip install discord.py`를 입력하여 discord.py 모듈을 설치합니다.
이 과정에서 asyncio, aiohttp 등의 부수적인 모듈까지 같이 설치되게 됩니다.
PATH를 체크하지 않으셨다면 `py -m pip install discord.py`를 입력하시면 설치됩니다.

모듈이 설치되었다면 해당 파일을 다운받은 후 실행시키면 됩니다.


# 버그 제보
이미 봇은 여러 차례의 검사를 통하여 발생할 수 있는 버그를 잡아내었습니다.
그럼에도 불구하고, 예기치 않은 버그가 발생할 경우, 
https://github.com/frin0911/discordpy-example/issues 에서 양식에 맞게 버그를 제보해주시기 바랍니다.

단순한 사용자의 문제라면 답변해드리지 않습니다.
